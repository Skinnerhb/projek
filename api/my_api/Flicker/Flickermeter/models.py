from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class LightI(models.Model):
    LightID = models.CharField(unique=True, max_length=50)
    LightType = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    UserID = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.LightID

class Data(models.Model):
    Broadband = models.FloatField()
    Infrared = models.FloatField()
    Illuminance = models.FloatField()
    FlickerModulation = models.FloatField()
    FlickerIndex = models.FloatField()
    LongFlickerModulation = models.FloatField()
    LongFlickerIndex = models.FloatField()
    Luminance = models.FloatField()
    Flux = models.FloatField()
    Time = models.FloatField()
    LightID = models.ForeignKey(LightI, on_delete = models.CASCADE)
    
    