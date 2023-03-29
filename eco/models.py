# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser
 

class CustomUser(AbstractUser):
    SEX = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
    )
    public_name = models.CharField(max_length=100)
    sex = models.CharField(choices=SEX, max_length=1)
    birth_date = models.DateField(null=True)
    locality = models.CharField(max_length=100, null=True)
    photo = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Admarea(models.Model):
    admarea_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class CategoryObjDict(models.Model):
    category_obj_id = models.AutoField(primary_key=True)#?
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Organizations(models.Model):
    inn = models.DecimalField(primary_key=True, max_digits=12, decimal_places=0, max_length=12)
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    phone_number = models.CharField(max_length=12) #Исправить


class StatusesDict(models.Model):
    status_id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Districts(models.Model):
    district_id = models.AutoField(primary_key=True)
    admarea_id = models.ForeignKey(Admarea, models.SET_NULL, null=True, blank=True)  
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class NatureObjects(models.Model):
    object_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    category_obj_id = models.ForeignKey(CategoryObjDict, models.SET_NULL, related_name='category', null=True)
    latitude_n = models.DecimalField(max_digits=8, decimal_places=6, max_length=9)  
    longitude_e = models.DecimalField(max_digits=8, decimal_places=6, max_length=9)
    admarea_id = models.ForeignKey(Admarea, models.SET_NULL, blank=True, null=True)
    district_id = models.OneToOneField(Districts, models.SET_NULL, blank=True, null=True)
    locality = models.CharField(max_length=256)
    transport_description = models.CharField(max_length=100)
    adress = models.CharField(max_length=256)
    organization_inn = models.OneToOneField(Organizations, models.SET_NULL, blank=True, null=True)
    has_parking = models.BooleanField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    schedule = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Events(models.Model):
    event_id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    status_id = models.ForeignKey(StatusesDict, models.SET_NULL, null=True)  
    adress = models.CharField(max_length=256)
    latitude_n = models.DecimalField(max_digits=8, decimal_places=6, max_length=9)  
    longitude_e = models.DecimalField(max_digits=8, decimal_places=6, max_length=9)  
    photo = models.ImageField(blank=True, null=True)  # This field type is a guess.
    time_start = models.DateTimeField()
    time_of_close = models.DateTimeField()

    def __str__(self):
        return self.name


class Routes(models.Model):
    DIFFICULT = (
        ('A', 'Очень легко'),
        ('B', 'Легко'),
        ('C', 'Средне'),
        ('D', 'Сложно'),
    )

    route_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    start_n = models.DecimalField(max_digits=8, decimal_places=6)  
    start_e = models.DecimalField(max_digits=7, decimal_places=5)  
    end_n = models.DecimalField(max_digits=8, decimal_places=6)  
    end_e = models.DecimalField(max_digits=7, decimal_places=5)  
    diffictulity_level = models.CharField(max_length=1, default='A', choices=DIFFICULT)  
    length = models.FloatField()
    duration = models.TextField()  # This field type is a guess.
    transport_description = models.CharField(max_length=100)
    locality = models.CharField(max_length=256)
    price = models.IntegerField()
    photo = models.ImageField(blank=True, null=True)  # This field type is a guess.

    def __str__(self):
        return self.name


class SortPoints(models.Model):
    point_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    admarea_id = models.ForeignKey(Admarea, models.SET_NULL, blank=True, null=True)
    district_id = models.OneToOneField(Districts, models.SET_NULL, blank=True, null=True)
    transport_description = models.CharField(max_length=100)
    adress = models.CharField(max_length=256)
    locality = models.CharField(max_length=256)
    description = models.CharField(max_length=100)
    latitude_n = models.DecimalField(max_digits=8, decimal_places=6, max_length=9)  
    longitude_e = models.DecimalField(max_digits=8, decimal_places=5, max_length=9)  
    organization_inn = models.OneToOneField(Organizations, models.CASCADE)
    schedule = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Favourites(models.Model):
    fav_id = models.AutoField(primary_key=True)  
    user_id = models.ForeignKey(CustomUser, models.CASCADE)  
    event_id = models.ForeignKey(Events, models.DO_NOTHING, blank=True, null=True)  
    object_id = models.ForeignKey(NatureObjects, models.DO_NOTHING, blank=True, null=True)  
    route_id = models.ForeignKey(Routes, models.DO_NOTHING, blank=True, null=True)  
    point_id = models.ForeignKey(SortPoints, models.DO_NOTHING, blank=True, null=True)  


class StatusesRDict(models.Model):
    status_id_r = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Reports(models.Model):
    report_id = models.AutoField(primary_key=True)  
    description = models.CharField(max_length=100)
    photo = models.ImageField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True)
    status_id_r = models.ForeignKey(StatusesRDict, models.DO_NOTHING)  
    event_id = models.ForeignKey(Events, models.DO_NOTHING, blank=True, null=True)  
    user_id = models.ForeignKey(CustomUser, models.DO_NOTHING, blank=True, null=True)  
    route_id = models.ForeignKey(Routes, models.DO_NOTHING, blank=True, null=True)
    object_id = models.ForeignKey(NatureObjects, models.DO_NOTHING, blank=True, null=True)
    point_id = models.ForeignKey(SortPoints, models.DO_NOTHING, blank=True, null=True)


class Rates(models.Model):
    rate_id = models.AutoField(primary_key=True)  
    report_id = models.ForeignKey(Reports, models.CASCADE)  
    rate1 = models.IntegerField()  
    rate2 = models.IntegerField()  
    rate3 = models.IntegerField()  


class WasteTypes(models.Model):
    waste_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    unit_of_waste = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Results(models.Model):
    result_id = models.AutoField(primary_key=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    report_id = models.ForeignKey(Reports, models.CASCADE)
    amount = models.DecimalField(max_digits=30, decimal_places=30)
    waste_id = models.ForeignKey(WasteTypes, models.CASCADE)
    aproved = models.BooleanField(blank=True, null=True) 


class EventsOnNatureObjects(models.Model):
    event_id = models.ForeignKey(Events, models.CASCADE)  
    object_id = models.ForeignKey(NatureObjects, models.CASCADE)  
    eo_id = models.AutoField(primary_key=True)  

    class Meta:
        unique_together = (('event_id', 'object_id'),)


class EventsOnRoutes(models.Model):
    event_id = models.ForeignKey(Events, models.CASCADE)  
    route_id = models.ForeignKey(Routes, models.CASCADE)


class PointTypes(models.Model):
    waste_id = models.ForeignKey(WasteTypes, models.CASCADE)  
    point_id = models.ForeignKey(SortPoints,  models.CASCADE)  


'''class WorkingHours(models.Model):
    DAYS = (
        ('Mon', 'Понедельник'),
        ('Tue', 'Вторник'),
        ('Wed', 'Среда'),
        ('Thu', 'Четверг'),
        ('Fri', 'Пятница'),
        ('Sat', 'Суббота'),
        ('Sun', 'Воскресенье'),
    )

    workin_hours_id = models.AutoField(db_column='workin_hoursID', primary_key=True)
    day_of_week = models.CharField(max_length=3, choices=DAYS)
    open_time = models.TimeField()
    close_time = models.TimeField()
    each = models.CharField(max_length=32)
    point_id = models.ForeignKey(SortPoints, models.CASCADE)

    def __str__(self):
        return self.day_of_week'''