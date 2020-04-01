from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.gis.db import models
from django.contrib.auth.models import User


# Create your models here.


class cases(models.Model):
    name = models.CharField(max_length=500)
    telephone = PhoneNumberField(
        blank=True, null=True, help_text="Contact phone number")
    address = models.CharField(max_length=500, blank=True, null=True)
    x = models.FloatField()
    y = models.FloatField()
    condition = models.CharField(max_length=500)
    age = models.IntegerField()
    sex = models.CharField(max_length=50)
    food_need = models.CharField(max_length=500, blank=True, null=True)
    hygine_need = models.CharField(max_length=500, blank=True, null=True)
    other_need = models.CharField(max_length=500, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    def __str__(self):
        return self.name


class volunteers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = PhoneNumberField(
        blank=True, null=True, help_text="Mobile phone number")
    landline = models.CharField(max_length=500, blank=True, null=True)

    created_time = models.DateTimeField(auto_now_add=True)
    servicescanprovide = models.CharField(max_length=5000)
    geom = models.GeometryField(blank=True, null=True)
    x = models.FloatField()
    y = models.FloatField()
    country = models.CharField(max_length=5000)
    address = models.CharField(max_length=5000)
    postal_code = models.IntegerField()

    def __str__(self):
        return self.user.username
