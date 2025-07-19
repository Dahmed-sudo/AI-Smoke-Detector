🚭 AI-Based Smoke Detection System Using OpenCV & Hand-Face Detection
This project is a real-time smoke detection system built with Python, OpenCV, cvzone, and AI-based gesture and facial landmark detection. It detects if a person is smoking (by analyzing hand-to-mouth motion) and triggers an audio alarm while logging the incident with a timestamp.

🎯 Features
🔍 Real-time smoke-like gesture detection using FaceMesh and HandTracking modules.

📢 Text-to-speech voice warning using gTTS and pygame.

📝 Incident logging with timestamp.

🔴 Visual alert with red frame and on-screen warning.

✅ Auto-reset when smoking gesture stops.

🗑️ Automatic cleanup of temporary audio files on exit.

📷 How It Works
Face Detection: Detects the user’s facial landmarks (especially mouth area).

Hand Detection: Detects hand position using a hand landmark detector.

Gesture Analysis: If hand approaches the mouth area within a defined distance → assumes smoking behavior.

Audio Warning: Plays a looped audio warning using pygame.mixer.

Logging: Saves the incident with timestamp in smoking_incidents.txt.

📁 Folder Structure
bash
Copier
Modifier
.
├── smoke_detection.py         # Main Python script
├── alarm.mp3                  # Audio file (auto-generated)
├── smoking_incidents.txt      # Log file (auto-generated)
├── README.md                  # Project documentation
✅ Requirements
Install the following dependencies:

bash
Copier
Modifier
pip install opencv-python cvzone pygame gTTS
▶️ How to Run
bash
Copier
Modifier
python smoke_detection.py
Then press q to quit the program.

🔊 Audio Alarm
If alarm.mp3 does not exist, the script will automatically generate it using Google Text-to-Speech (gTTS) with the message:

"Smoking detected, please don't smoke here. Warning! Smoking is not allowed in this area."

🗃️ Incident Logging
Each time a smoking gesture is detected, an entry like the following is added to smoking_incidents.txt:

yaml
Copier
Modifier
Smoking detected at 2025-07-19 22:48:33
📌 Notes
The detection is gesture-based, not based on actual smoke/fumes.

Ideal for controlled environments (e.g. indoors, offices, schools).

Improve accuracy by adjusting detection threshold (distance < 40).

🧠 Built With
OpenCV

cvzone

pygame

gTTS

📜 License
This project is open-source and free to use for educational and non-commercial purposes.

