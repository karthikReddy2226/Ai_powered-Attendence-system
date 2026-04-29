from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
import cv2
from .face_utils import encode_known_faces, recognize_face

known_encodings, known_names = encode_known_faces()

@api_view(['POST'])
def mark_attendance(request):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return JsonResponse({'error': 'Camera Error'}, status=500)

    name = recognize_face(frame, known_encodings, known_names)

    if name:
        return JsonResponse({'status': 'success', 'name': name})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Face not recognized'})
    
from rest_framework import viewsets
from .models import Attendance
from .serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by('-time')
    serializer_class = AttendanceSerializer


# views.py (Django)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Attendance
import face_recognition
import pickle
from django.core.files.uploadedfile import InMemoryUploadedFile
import numpy as np
from PIL import Image
import io

with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

@api_view(['POST'])
def detect_face_upload(request):
    f = request.FILES.get('image')
    if not f:
        return Response({"error": "no image"}, status=400)
    img = Image.open(f)
    rgb = np.array(img.convert('RGB'))
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)
    name = None
    for encoding in encodings:
        matches = face_recognition.compare_faces(data['encodings'], encoding)
        if True in matches:
            matched_idxs = [i for i,b in enumerate(matches) if b]
            counts = {}
            for i in matched_idxs:
                n = data['names'][i]
                counts[n] = counts.get(n, 0) + 1
            name = max(counts, key=counts.get)
            break
    if name:
        Attendance.objects.create(name=name)
        return Response({"status":"success","name":name})
    return Response({"status":"unknown"})
