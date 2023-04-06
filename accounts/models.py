import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class ChemMLUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patronymic = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Отчество"
    )

    def __str__(self):
        return self.email

    class Meta:
        indexes = [models.Index(fields=["id"])]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
