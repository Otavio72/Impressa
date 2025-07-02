from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# Modelo de usuário personalizado que herda todos os campos do AbstractUser.
class CustomUser(AbstractUser):
    pass 

