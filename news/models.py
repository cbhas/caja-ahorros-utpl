from django.db import models

# Create your models here.
class New(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField()
    place = models.CharField(max_length=100)
    image = models.ImageField(upload_to='news/')
    created_at = models.DateTimeField(auto_created=True, null=True)

    def __str__(self):
        return self.title