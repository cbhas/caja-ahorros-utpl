from django.db import models

from events.models import Event
from django.conf import settings

# Create your models here.
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    puchase_date = models.DateField(auto_now_add=True)

