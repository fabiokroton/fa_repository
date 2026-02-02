from django.db import models

class SiteSettings(models.Model):
    registration_open = models.BooleanField(
        default=True,
        verbose_name="Registrazioni aperte"
    )

    def __str__(self):
        return "Impostazioni del sito"

    def save(self, *args, **kwargs):
        # Garantisce che esista un solo record
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        # Recupera l’unico record, o lo crea se non esiste
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
