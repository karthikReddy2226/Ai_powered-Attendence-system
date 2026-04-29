from django.db import models

class Attendance(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.time}"
