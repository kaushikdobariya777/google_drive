from django.db import models


class GoogleAuthToken(models.Model):
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)

    def __str__(self):
        return self.name
