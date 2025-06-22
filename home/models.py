from django.db import models
from users.models import CustomUser


class DashboardLog(models.Model):
    client = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='home')
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
