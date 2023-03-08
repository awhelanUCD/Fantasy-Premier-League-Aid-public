from django.db import models

# Create your models here.
# Create your models here.
class Features(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    #technology = models.CharField(max_length=20)
    image = models.ImageField(upload_to="img/")
    urlField=models.CharField(max_length=100, default="#")
