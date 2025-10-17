from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Board(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Pin(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='pins')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pins/')
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
