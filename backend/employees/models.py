from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):

    dept = models.CharField(max_length=50, null=True, blank=True)

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    joining_date = models.DateField()

    profile = models.CharField(max_length=100, null=True, blank=True)

    country  = models.CharField(max_length=100, null=True, blank=True)

    state = models.CharField(max_length=50)

    city = models.CharField(max_length=50)

    pincode = models.CharField(max_length=10)

    contact_no = models.CharField(max_length=15)

    email = models.EmailField()

    def __str__(self):
        return self.first_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username