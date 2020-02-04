from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/", default='avatars/default.jpg')

    class Meta:
        verbose_name = "profil"

    def __str__(self):
        return self.user.username