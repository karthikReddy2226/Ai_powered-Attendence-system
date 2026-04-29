import os
import face_recognition
import pickle

KNOWN_FACES_DIR = "known_faces"
encodings = []
names = []

for name in os.listdir(KNOWN_FACES_DIR):
    person_dir = os.path.join(KNOWN_FACES_DIR, name)
    if not os.path.isdir(person_dir):
        continue
    for filename in os.listdir(person_dir):
        filepath = os.path.join(person_dir, filename)
        image = face_recognition.load_image_file(filepath)
        face_enc = face_recognition.face_encodings(image)
        if face_enc:
            encodings.append(face_enc[0])
            names.append(name)

data = {"encodings": encodings, "names": names}
with open("encodings.pkl", "wb") as f:
    pickle.dump(data, f)

print("Training complete. Encodings saved.")
