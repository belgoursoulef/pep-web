import os
import time
import datetime
import threading

# Set low-latency FFMPEG environment options BEFORE importing OpenCV
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp|fflags;nobuffer|flags;low_delay"

import cv2
import mysql.connector
from flask import Flask, Response

# Database connection details
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'rootpassword')
DB_NAME = os.environ.get('DB_NAME', 'carhorizon')

# Global frames dictionary
camera_frames = {
    "Camera 1 (Entrance)": None,
    "Camera 2 (Garage)": None
}

EMPLOYEES = {
    "EMP001": {"nom": "BELGOUR", "prenom": "Aicha Soulef", "service": "IT"},
    "EMP002": {"nom": "ROLIN", "prenom": "Tom", "service": "Production"},
    "EMP003": {"nom": "Balde", "prenom": "Mamadou", "service": "Administratif"},
    "EMP004": {"nom": "Diahouila", "prenom": "Ferancel Iverson", "service": "Production"},
    "EMP005": {"nom": "Jacaton", "prenom": "Paul", "service": "IT"}
}

def insert_device_log(device_name, log_level, message):
    """Inserts a device log into the shared MySQL database."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO device_logs (device_name, log_level, message) VALUES (%s, %s, %s)",
                (device_name, log_level, message)
            )
            connection.commit()
            print(f"Logged: [{device_name}] {log_level} - {message}")
    except Exception as e:
        print(f"Error logging to DB in thread: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def run_badge_scanner():
    """Background thread to capture from Camera 1 and scan badges."""
    camera_url = "rtsp://admin:Vivotek29@192.168.32.98/live.sdp"
    print("Initializing Camera 1 Capture...")
    cap = cv2.VideoCapture(camera_url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    qr_detector = cv2.QRCodeDetector()
    dernier_badge = None
    temps_dernier_scan = 0

    print("=== Background Badge Scanner thread started ===")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera 1 (Entrance) stream disconnected. Reconnecting in 5s...")
            time.sleep(5)
            cap = cv2.VideoCapture(camera_url)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            continue

        # Encode and store frame for the web client
        ret_jpg, jpeg = cv2.imencode('.jpg', frame)
        if ret_jpg:
            camera_frames["Camera 1 (Entrance)"] = jpeg.tobytes()

        # QR scanning
        data, bbox, _ = qr_detector.detectAndDecode(frame)
        if data:
            temps_actuel = time.time()
            if data != dernier_badge or (temps_actuel - temps_dernier_scan > 3):
                dernier_badge = data
                temps_dernier_scan = temps_actuel
                horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if data in EMPLOYEES:
                    emp = EMPLOYEES[data]
                    statut = "AUTORISE"
                    db_message = f"Access GRANTED - {emp['prenom']} {emp['nom']} ({emp['service']})"
                    log_level = "INFO"
                else:
                    statut = "REFUSE"
                    db_message = f"Access DENIED - Unknown badge scanned: {data}"
                    log_level = "WARNING"

                print(f"[{horodatage}] {statut} : {db_message}")
                insert_device_log("Camera 1 (Entrance)", log_level, db_message)
                
                try:
                    with open("historique_acces.csv", "a", encoding="utf-8") as f:
                        f.write(f"{horodatage},{data},{statut}\n")
                except Exception as e:
                    print(f"Error writing access CSV: {e}")

        time.sleep(0.01)

    cap.release()

def run_intrusion_alarm():
    """Background thread to capture from Camera 2 and detect motion/intrusions."""
    url_cam2 = "rtsp://admin:Vivotek29@192.168.32.99/live.sdp"
    HEURE_DEBUT_INTERDIT = 20
    HEURE_FIN_INTERDIT = 7

    print("Initializing Camera 2 Capture...")
    cap2 = cv2.VideoCapture(url_cam2)
    cap2.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    fgbg = cv2.createBackgroundSubtractorMOG2()

    print("=== Background Intrusion Alarm thread started ===")

    def est_en_horaire_interdit():
        heure_actuelle = datetime.datetime.now().hour
        return heure_actuelle >= HEURE_DEBUT_INTERDIT or heure_actuelle < HEURE_FIN_INTERDIT

    while True:
        ret2, frame2 = cap2.read()
        if not ret2:
            print("Camera 2 (Garage) stream disconnected. Reconnecting in 5s...")
            time.sleep(5)
            cap2 = cv2.VideoCapture(url_cam2)
            cap2.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            continue

        # Encode and store frame for the web client
        ret_jpg, jpeg = cv2.imencode('.jpg', frame2)
        if ret_jpg:
            camera_frames["Camera 2 (Garage)"] = jpeg.tobytes()

        # Motion detection
        fgmask = fgbg.apply(frame2)
        _, thresh = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
        
        if cv2.countNonZero(thresh) > 5000:
            if est_en_horaire_interdit():
                horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{horodatage}] ALERTE INTRUSION detected")
                insert_device_log("Camera 2 (Garage)", "ALERT", "Intrusion detected - Motion detected during off-hours!")
                
                try:
                    with open("historique_intrusion.csv", "a", encoding="utf-8") as f:
                        f.write(f"{horodatage},INTRUSION\n")
                except Exception as e:
                    print(f"Error writing intrusion CSV: {e}")

        time.sleep(0.01)

    cap2.release()

# Flask App setup
app = Flask(__name__)

def gen_video_feed(camera_name):
    """Generator for MJPEG stream."""
    while True:
        frame_bytes = camera_frames.get(camera_name)
        if frame_bytes is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            time.sleep(0.1)
        # Yield very fast to maintain zero-latency
        time.sleep(0.01)

@app.route('/video_feed/1')
def video_feed_1():
    return Response(gen_video_feed("Camera 1 (Entrance)"),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed/2')
def video_feed_2():
    return Response(gen_video_feed("Camera 2 (Garage)"),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start threads in background
    t1 = threading.Thread(target=run_badge_scanner, daemon=True)
    t2 = threading.Thread(target=run_intrusion_alarm, daemon=True)
    t1.start()
    t2.start()

    # Serve camera endpoints on port 5001
    app.run(host='0.0.0.0', port=5001, debug=False)
