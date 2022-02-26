from PIL import Image
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Ticket(models.Model):
    def __str__(self):
        return f'{self.title, self.description}'
    titre = models.CharField(max_length=128, blank=True)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True, blank=True)
    rated = models.BooleanField(default=False)

    IMAGE_MAX_SIZE = (400, 400)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()


class Review(models.Model):
    def __str__(self):
        return f'{self.headline, self.ticket, self.user}'
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, blank=True)
    note = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])

    accroche = models.CharField(max_length=128)
    critique = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
