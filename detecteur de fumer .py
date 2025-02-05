# Importation des bibliothèques nécessaires
import cv2  # Pour la capture vidéo et le traitement d'images
import cvzone  # Pour des fonctionnalités supplémentaires comme l'affichage de texte
from cvzone.FaceMeshModule import FaceMeshDetector  # Pour détecter les maillages faciaux
from cvzone.HandTrackingModule import HandDetector  # Pour détecter les mains
import os  # Pour gérer les fichiers temporaires
import pygame  # Pour la lecture audio
import time  # Pour gérer le temps
import datetime  # Pour l'horodatage des incidents
from gtts import gTTS  # Pour la synthèse vocaleq

# Initialisation de pygame pour la lecture audio
pygame.mixer.init()

# Initialisation des détecteurs
Hand_Detector = HandDetector()  # Détecteur de mains
MeshDetector = FaceMeshDetector()  # Détecteur de maillages faciaux

# Ouverture de la caméra (0 est généralement la caméra par défaut)
video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Erreur: Impossible d'ouvrir la caméra.")
    exit()

# Variables pour stocker les positions des points détectés
point11X = point11Y = 0

# Variables pour gérer l'alarme persistante
alarm_active = False  # Indique si l'alarme est active
alarm_start_time = 0  # Temps de début de l'alarme
alarm_cooldown = 5  # Temps en secondes avant de pouvoir relancer l'alarme

# Fichier pour enregistrer les incidents
incident_log = "smoking_incidents.txt"

# Chemin vers le fichier audio d'alarme
alarm_sound = "alarm.mp3"  # Remplacez par le chemin de votre fichier audio

# Texte à convertir en audio
text = "Smoking detected, please don't smoke here. Warning! Smoking is not allowed in this area."

# Créer un fichier audio à partir du texte (une seule fois au début)
if not os.path.exists(alarm_sound):
    try:
        tts = gTTS(text=text, lang='en')  # Créer un fichier audio
        tts.save(alarm_sound)  # Sauvegarder le fichier audio
        print(f"Fichier audio créé : {alarm_sound}")
    except Exception as e:
        print(f"Erreur lors de la création du fichier audio : {e}")

# Fonction pour jouer un fichier audio avec pygame
def play_audio(file_path, loop=0):
    """
    Joue un fichier audio en boucle.
    :param file_path: Chemin du fichier audio
    :param loop: Nombre de boucles (-1 pour une boucle infinie)
    """
    try:
        pygame.mixer.music.load(file_path)  # Charger le fichier audio
        pygame.mixer.music.play(loop)  # Jouer le fichier audio
    except Exception as e:
        print(f"Erreur lors de la lecture audio : {e}")

# Fonction pour arrêter la lecture audio
def stop_audio():
    """
    Arrête la lecture audio en cours.
    """
    try:
        pygame.mixer.music.stop()  # Arrêter la lecture audio
    except Exception as e:
        print(f"Erreur lors de l'arrêt de la lecture audio : {e}")

# Fonction pour enregistrer un incident dans le fichier log
def log_incident():
    """
    Enregistre un incident de détection de fumée dans un fichier log.
    """
    with open(incident_log, "a") as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"Smoking detected at {timestamp}\n")

# Boucle principale de traitement vidéo
while True:
    # Lire une frame de la caméra
    ret, image = video.read()
    if not ret:
        print("Erreur: Impossible de lire la frame de la caméra.")
        continue  # Passer à l'itération suivante au lieu de quitter

    # Détecter les maillages faciaux (sans dessiner les points)
    img, faces = MeshDetector.findFaceMesh(image, draw=False)  # draw=False pour ne pas afficher les points

    # Détecter les mains (avec dessin des points)
    results = Hand_Detector.findHands(image, draw=True)  # draw=True pour afficher les points

    # Si un visage est détecté
    if faces:
        point14 = faces[0][14]  # Point de la lèvre

        # Si une main est détectée
        if results and len(results[0]) > 0:
            landmarks = results[0][0]['lmList']
            point11X, point11Y = landmarks[11][0], landmarks[11][1]  # Point de la main

            # Calculer la distance entre le point de la main et le point de la lèvre
            distance = MeshDetector.findDistance((point11X, point11Y), (point14[0], point14[1]))[0]

            # Afficher un message en fonction de la distance
            if distance < 40:
                message = "Smoking Detected! Please don't smoke here."
                alarm_color = (0, 0, 255)  # Rouge pour l'alarme

                # Activer l'alarme si elle n'est pas déjà active
                if not alarm_active:
                    try:
                        play_audio(alarm_sound, loop=-1)  # Jouer l'alarme sonore en boucle
                        alarm_active = True
                        alarm_start_time = time.time()
                        log_incident()  # Enregistrer l'incident
                    except Exception as e:
                        print(f"Erreur lors de la lecture audio : {e}")
            else:
                message = "No smoking detected."
                alarm_color = (0, 255, 0)  # Vert pour l'état normal

                # Désactiver l'alarme si la situation est résolue
                if alarm_active:
                    stop_audio()  # Arrêter la lecture audio
                    alarm_active = False

            # Afficher le message à l'écran
            cvzone.putTextRect(image, message, (30, 50), colorR=alarm_color)

            # Dessiner un cadre rouge autour de l'écran si l'alarme est active
            if alarm_active:
                cv2.rectangle(image, (0, 0), (image.shape[1], image.shape[0]), (0, 0, 255), 10)
        else:
            cvzone.putTextRect(image, 'No hand detected', (30, 50))
    else:
        cvzone.putTextRect(image, 'No face detected', (30, 50))

    # Afficher l'image
    cv2.imshow('Camera', image)

    # Appuyez sur 'q' pour quitter
    if cv2.waitKey(20) == ord('q'):
        break

# Libérer la caméra et fermer les fenêtres
video.release()
cv2.destroyAllWindows()

# Arrêter la lecture audio avant de quitter
stop_audio()

# Supprimer le fichier audio temporaire après utilisation 
if os.path.exists(alarm_sound):
    os.remove(alarm_sound)
    print(f"Fichier audio supprimé : {alarm_sound}")