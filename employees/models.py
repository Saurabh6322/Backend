from django.db import models

# Create your models here.
class Employee(models.Model):

    dept_id = models.IntegerField()

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    joining_date = models.DateField()

    street = models.CharField(max_length=100)

    city = models.CharField(max_length=50)

    state = models.CharField(max_length=50)

    pincode = models.CharField(max_length=10)

    contact_no = models.CharField(max_length=15)

    email = models.EmailField()

    def __str__(self):
        return self.first_name