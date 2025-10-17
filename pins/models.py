from django.db import models
from django.contrib.auth.models import User
from boards.models import Board

class Pin(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='pins/')
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pins')

    def __str__(self):
        return self.title
