from django.db import models
from django.utils import timezone


class Items(models.Model):
    item = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=200)

    def __str__(self):
        return self.item

class User(models.Model):
    cellnumber = models.CharField(max_length=20)
    landlinenumber =  models.CharField(max_length=20)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    inneed = models.BooleanField(default=False)
    helper = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.cellnumber

   
class UserVerify(models.Model):
    ID1 = models.CharField(max_length=100)
    ID2 = models.CharField(max_length=100)
    ID3 = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.cellnumber

