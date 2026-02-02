from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    class_group = models.CharField(max_length=10, verbose_name="Classe")
    section = models.CharField(max_length=5, verbose_name="Sezione")
    school = models.CharField(max_length=100, default="Colombo", verbose_name="Scuola")

    data_consent = models.BooleanField(
        default=False,
        help_text="Consenso al trattamento dei dati personali"
    )
