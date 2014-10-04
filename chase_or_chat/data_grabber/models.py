from django.db import models

class laptop(models.Model):
    url = models.CharField(max_length=120)
    title = models.CharField(max_length=100)
    cpu = models.CharField(max_length=50)
    ram = models.CharField(max_length=30)
    hardware = models.CharField(max_length=40)
    screen = models.CharField(max_length=40)
    price = models.IntegerField()
    else_spec = models.CharField(max_length=300)
    picture = models.CharField(max_length=300)

