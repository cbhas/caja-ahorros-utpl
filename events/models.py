from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    date = models.DateField()
    place = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='events/')
    created_at = models.DateTimeField(auto_created=True, null=True)
    available_tickets = models.IntegerField(default=0)

    def __str__(self):
        return self.name