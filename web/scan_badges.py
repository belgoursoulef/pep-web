import cv2
import datetime
import time
import os
import mysql.connector
from mysql.connector import Error

# Configuration de la base de données
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', 33066 if DB_HOST == 'localhost' else 3306))
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'rootpassword')
DB_NAME = os.environ.get('DB_NAME', 'carhorizon')

def log_to_db(device_name, log_level, message):
    """Insère un log d'événement dans la base de données MySQL du site."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
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
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Erreur de connexion à la base de données : {e}")

# 1. Base de données locale de tes 5 employés autorisés
EMPLOYEES = {
    "EMP001": {"nom": "BELGOUR", "prenom": "Aicha Soulef", "service": "IT"},
    "EMP002": {"nom": "ROLIN", "prenom": "Tom", "service": "Production"},
    "EMP003": {"nom": "Balde", "prenom": "Mamadou", "service": "Administratif"},
    "EMP004": {"nom": "Diahouila", "prenom": "Ferancel Iverson", "service": "Production"},
    "EMP005": {"nom": "Jacaton", "prenom": "Paul", "service": "IT"}
}

# 2. Configuration du flux réseau (Caméra IP8166 - Entrée)

camera_url = "rtsp://admin:Vivotek29@192.168.32.98/live.sdp"
cap = cv2.VideoCapture(camera_url)

qr_detector = cv2.QRCodeDetector()
dernier_badge = None
temps_dernier_scan = 0

print("=== Système de filtrage des accès actif ===")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur : Connexion au flux RTSP perdue.")
        break

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
                color = (0, 255, 0)
                log = f"[{horodatage}] {statut} : {emp['prenom']} {emp['nom']}"
                db_message = f"Access GRANTED - {emp['prenom']} {emp['nom']} ({emp['service']})"
                log_level = "INFO"
            else:
                statut = "REFUSE"
                color = (0, 0, 255)
                log = f"[{horodatage}] {statut} : Badge inconnu ({data})"
                db_message = f"Access DENIED - Unknown badge scanned: {data}"
                log_level = "WARNING"

            print(log)
            # Envoi du log à la base de données pour affichage sur le site web
            log_to_db("Camera 1 (Entrance)", log_level, db_message)

            with open("historique_acces.csv", "a", encoding="utf-8") as f:
                f.write(f"{horodatage},{data},{statut}\n")

        if bbox is not None and len(bbox) > 0:
            pts = bbox[0].astype(int)
            for i in range(len(pts)):
                cv2.line(frame, tuple(pts[i]), tuple(pts[(i+1) % len(pts)]), color, 3)
            cv2.putText(frame, statut, (pts[0][0], pts[0][1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Controle Acces - Caméra Entrée", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()