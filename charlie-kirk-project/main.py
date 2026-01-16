import cv2
import pygame
import os
import time

# --- CONFIGURATION ---
# How many seconds of "looking away" before Charlie speaks?
DOOMSCROLL_LIMIT = 2 

def main():
    # 1. Setup Sound
    pygame.mixer.init()
    
    # Automatically find the MP3 file in the folder
    sound_files = [f for f in os.listdir('.') if f.endswith('.mp3')]
    if not sound_files:
        print("ERROR: No .mp3 file found! Make sure the mp3 is in this folder.")
        return
    
    sound_path = sound_files[0]
    print(f"Loaded audio: {sound_path}")
    pygame.mixer.music.load(sound_path)

    # 2. Setup Camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam.")
        return

    # 3. Setup Lightweight Face Detection (Built-in to OpenCV)
    try:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    except AttributeError:
        print("Error: Could not find face detection data. Make sure opencv-python is installed.")
        return

    print("--- CHARLIE IS WATCHING (LITE MODE) ---")
    print("Press 'q' to quit.")

    last_seen_face_time = time.time()
    is_playing = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        current_time = time.time()

        if len(faces) > 0:
            last_seen_face_time = current_time
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            if is_playing:
                pygame.mixer.music.stop()
                is_playing = False
                print("Face detected - Silencing.")
        else:
            if (current_time - last_seen_face_time) > DOOMSCROLL_LIMIT and not is_playing:
                print("Doomscrolling! Playing audio...")
                pygame.mixer.music.play(-1)
                is_playing = True

        cv2.imshow('Charlie (Lite)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
