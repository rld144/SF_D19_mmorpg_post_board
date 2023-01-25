from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models


class SignupOtc(models.Model):
    username = models.CharField(max_length=20)
    password1 = models.CharField(max_length=20)
    password2 = models.CharField(max_length=20)
    email = models.EmailField()
    otc = models.IntegerField()
    its_confirmed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


