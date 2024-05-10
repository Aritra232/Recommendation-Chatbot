from django.contrib.auth.models import User
from django.db import models

class userinfo(models.Model):
    username = models.CharField(max_length=20,null=True)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nid = models.CharField(max_length=250,null=True)
    gender = models.CharField(
        max_length=6,
        choices=[('Male','Male'),('FeMale','FeMale')]
    )

    def __str__(self):
        return self.user.username
