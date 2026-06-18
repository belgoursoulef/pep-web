import cv2
import datetime
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

# 1. Configuration
# URL de ta caméra Fisheye 360°
url_cam2 = "rtsp://admin:Vivotek29@192.168.32.99/live.sdp"
HEURE_DEBUT_INTERDIT = 20
HEURE_FIN_INTERDIT = 7

# Initialisation du flux et du détecteur
cap2 = cv2.VideoCapture(url_cam2)
fgbg = cv2.createBackgroundSubtractorMOG2()

print("Système de détection d'intrusion actif. Appuyez sur 'q' pour quitter.")

def est_en_horaire_interdit():
    heure_actuelle = datetime.datetime.now().hour
    return heure_actuelle >= HEURE_DEBUT_INTERDIT or heure_actuelle < HEURE_FIN_INTERDIT

while True:
    ret2, frame2 = cap2.read()
    if not ret2:
        break

    # Détection de mouvement
    fgmask = fgbg.apply(frame2)
    _, thresh = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    
    # Si le mouvement est significatif
    if cv2.countNonZero(thresh) > 5000:
        if est_en_horaire_interdit():
            horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"[{horodatage}] ALERTE INTRUSION"
            print(message)
            
            # Envoi du log à la base de données pour affichage sur le site web
            log_to_db("Camera 2 (Garage)", "ALERT", "Intrusion detected - Motion detected during off-hours!")
            
            # Enregistrement dans le journal
            with open("historique_intrusion.csv", "a", encoding="utf-8") as f:
                f.write(f"{horodatage},INTRUSION\n")
            
            # Affichage visuel de l'alerte
            cv2.putText(frame2, "INTRUSION !", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Surveillance 360 - Alerte Intrusion", frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap2.release()
cv2.destroyAllWindows()