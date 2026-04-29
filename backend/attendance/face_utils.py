import face_recognition
import cv2
import numpy as np
import os

KNOWN_FACES_DIR = "known_faces"
TOLERANCE = 0.6

def encode_known_faces():
    known_encodings = []
    known_names = []

    for name in os.listdir(KNOWN_FACES_DIR):
        for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
            image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
            encodings = face_recognition.face_encodings(image)
            if len(encodings) > 0:
                encoding = encodings[0]
            else:
                print(f"⚠ No face found in {filename}, skipping.")
            continue
    
    return known_encodings, known_names

def recognize_face(frame, known_encodings, known_names):
    rgb_frame = frame[:, :, ::-1]
    locations = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame, locations)

    for encoding, location in zip(encodings, locations):
        results = face_recognition.compare_faces(known_encodings, encoding, TOLERANCE)
        if True in results:
            match = known_names[results.index(True)]
            return match
    return None
