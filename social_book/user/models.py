from django.db import models

class userDetails(models.Model):
    email = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
