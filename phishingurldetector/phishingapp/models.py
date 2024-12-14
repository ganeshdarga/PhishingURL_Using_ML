from django.db import models

from django.db import models
import datetime

class phishing(models.Model):
    phishing_URL = models.CharField(max_length=300,unique=True)
    type=models.IntegerField()


    def __str__(self):
        return f"{self.phishing_URL} - {self.type}"  

    

# Create your models here.
