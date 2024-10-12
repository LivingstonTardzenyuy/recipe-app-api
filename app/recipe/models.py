from django.db import models
from django.conf import settings 

# Create your models here.
class Recipe(models.Model):
    """Recipe model """
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    link = models.CharField(max_length=255, blank=True)
    
    
    def __str__(self):
        return self.title