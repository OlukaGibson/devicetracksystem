from django.db import models

# Create your models here.
class ThingSpeakData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}, Timestamp: {self.timestamp}"
