import face_recognition
import cv2
import pickle
import numpy as np
import csv
from datetime import datetime

# Load encodings
with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

# CSV file to save attendance
csv_filename = "attendance.csv"

# Create file with header if not exists
try:
    with open(csv_filename, "x", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Time"])
except FileExistsError:
    pass

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in current frame
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        if True in matches:
            matched_idxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matched_idxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

        names.append(name)

        # Save attendance if recognized and not already marked in this session
        if name != "Unknown":
            with open(csv_filename, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    # Draw boxes & names
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

from attendance.models import Attendance

if name != "Unknown":
    Attendance.objects.create(name=name)

