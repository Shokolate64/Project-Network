from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo de Usuario
class User(AbstractUser):
    pass

# Modelo para los Posts
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}..."

# Modelo para Seguimiento de Usuarios
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"
