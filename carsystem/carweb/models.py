from django.db import models

# Create your models here.

class CarData(models.Model):
    sale_date = models.CharField(max_length=255, blank=True, null=True)
    car_class = models.CharField(max_length=255, blank=True, null=True)
    sale_qut = models.CharField(max_length=255, blank=True, null=True)
    compartment = models.CharField(max_length=255, blank=True, null=True)
    tr = models.CharField(db_column='TR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gearbox_type = models.CharField(max_length=255, blank=True, null=True)
    displacement = models.CharField(max_length=255, blank=True, null=True)
    charge = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    driven_type = models.CharField(max_length=255, blank=True, null=True)
    fuel_type = models.CharField(max_length=255, blank=True, null=True)
    newenergy = models.CharField(max_length=255, blank=True, null=True)
    emission = models.CharField(max_length=255, blank=True, null=True)
    mvp = models.CharField(max_length=255, blank=True, null=True)
    luxurious = models.CharField(max_length=255, blank=True, null=True)
    power = models.CharField(max_length=255, blank=True, null=True)
    cylinder = models.CharField(max_length=255, blank=True, null=True)
    engine = models.CharField(max_length=255, blank=True, null=True)
    car_len = models.CharField(max_length=255, blank=True, null=True)
    car_width = models.CharField(max_length=255, blank=True, null=True)
    car_height = models.CharField(max_length=255, blank=True, null=True)
    total_quality = models.CharField(max_length=255, blank=True, null=True)
    equipment_quality = models.CharField(max_length=255, blank=True, null=True)
    rated_passenger = models.CharField(max_length=255, blank=True, null=True)
    wheelbase = models.CharField(max_length=255, blank=True, null=True)
    front_track = models.CharField(max_length=255, blank=True, null=True)
    rear_track = models.CharField(max_length=255, blank=True, null=True)


class Username(models.Model):
    user_name = models.CharField(unique=True, max_length=45)
    user_password = models.CharField(max_length=45)
    user_photo = models.ImageField(upload_to='')


class Carname(models.Model):
    car_name = models.CharField(max_length=255, blank=True, null=True)
    class_id = models.CharField(max_length=255, blank=True, null=True)
    car_url = models.ImageField(upload_to='car/')


class SaleData(models.Model):
    sale_date = models.CharField(max_length=255,blank=True, null=True)
    class_id = models.CharField(max_length=255,blank=True, null=True)
    sale_num = models.IntegerField()



