from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

class Review(models.Model):
    name = models.CharField(max_length=60)
    
    text = models.TextField(max_length=600)

    stars = models.SmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    date = models.CharField(max_length=30)

# Create your models here.
