# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator



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
    admarea_id = models.ForeignKey(Admarea, models.SET_NULL, null=True, blank=True, related_name='districts')  
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Favourites(models.Model):
    fav_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, models.CASCADE, related_name='favourites')  
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class StatusesRDict(models.Model):
    status_id_r = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class WasteTypes(models.Model):
    waste_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    unit_of_waste = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Reports(models.Model):
    report_id = models.AutoField(primary_key=True)  
    description = models.CharField(max_length=100)
    photo = models.ImageField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True)
    status_id_r = models.ForeignKey(StatusesRDict, models.DO_NOTHING, related_name='reports')  
    user_id = models.ForeignKey(CustomUser, models.CASCADE, related_name='reports')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class SortPoints(models.Model):
    point_id = models.AutoField(primary_key=True)
    photo = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=64)
    admarea_id = models.ForeignKey(Admarea, models.SET_NULL, blank=True, null=True, related_name='sort_points')
    district_id = models.OneToOneField(Districts, models.SET_NULL, blank=True, null=True)
    transport_description = models.CharField(max_length=100)
    adress = models.CharField(max_length=256)
    locality = models.CharField(max_length=256)
    description = models.CharField(max_length=100)
    latitude_n = models.DecimalField(max_digits=8, decimal_places=6, max_length=9)  
    longitude_e = models.DecimalField(max_digits=8, decimal_places=5, max_length=9)  
    organization_inn = models.OneToOneField(Organizations, models.CASCADE)
    schedule = models.CharField(max_length=100, blank=True, null=True)
    reports = GenericRelation(Reports)
    favourites = GenericRelation(Favourites)
    wast_types = models.ManyToManyField(WasteTypes)

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
    reports = GenericRelation(Reports, related_query_name='routes')
    favourites = GenericRelation(Favourites)

    def __str__(self):
        return self.name


class NatureObjects(models.Model):
    object_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    category_obj_id = models.ForeignKey(CategoryObjDict, models.SET_NULL, related_name='nature_objects', null=True)
    latitude_n = models.DecimalField(max_digits=8, decimal_places=6, max_length=9)  
    longitude_e = models.DecimalField(max_digits=8, decimal_places=6, max_length=9)
    admarea_id = models.ForeignKey(Admarea, models.SET_NULL, blank=True, null=True, related_name='nature_objects')
    district_id = models.OneToOneField(Districts, models.SET_NULL, blank=True, null=True)
    locality = models.CharField(max_length=256)
    transport_description = models.CharField(max_length=100)
    adress = models.CharField(max_length=256)
    organization_inn = models.OneToOneField(Organizations, models.SET_NULL, blank=True, null=True)
    has_parking = models.BooleanField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    schedule = models.CharField(max_length=100, blank=True, null=True)
    reports = GenericRelation(Reports, related_query_name='nature_object')
    favourites = GenericRelation(Favourites)

    def __str__(self):
        return self.name


class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    status_id = models.ForeignKey(StatusesDict, models.SET_NULL, null=True, related_name='events')  
    adress = models.CharField(max_length=256)
    latitude_n = models.DecimalField(max_digits=8, decimal_places=6, max_length=9)  
    longitude_e = models.DecimalField(max_digits=8, decimal_places=6, max_length=9)  
    photo = models.ImageField(blank=True, null=True)  # This field type is a guess.
    time_start = models.DateTimeField()
    time_of_close = models.DateTimeField()
    reports = GenericRelation(Reports, related_query_name='events')
    favourites = GenericRelation(Favourites)
    nature_objects = models.ManyToManyField(NatureObjects, blank=True)
    routes = models.ManyToManyField(Routes, blank=True)

    def __str__(self):
        return self.name


class Rates(models.Model):
    rate_id = models.AutoField(primary_key=True)  
    report_id = models.OneToOneField(Reports, models.CASCADE, related_name='rates')  
    availability = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    beauty = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    purity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


class Results(models.Model):
    result_id = models.AutoField(primary_key=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    report_id = models.ForeignKey(Reports, models.CASCADE, related_name='results')
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    waste_id = models.ForeignKey(WasteTypes, models.CASCADE, related_name='results')
    aproved = models.BooleanField(blank=True, null=True) 


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