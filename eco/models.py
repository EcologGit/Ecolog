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
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    phone_number_validator = RegexValidator(
        regex=r"\+?(?:7|8)9\d{9}", message="not valid phone number!"
    )
    SEX = (
        ("M", "Мужской"),
        ("F", "Женский"),
    )
    public_name = models.CharField(max_length=100)
    sex = models.CharField(choices=SEX, max_length=1)
    birth_date = models.DateField(null=True, blank=True)
    locality = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(blank=True, upload_to="user/", max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(
        max_length=12, validators=(phone_number_validator,), null=True, blank=True
    )
    kind_of_activity = models.CharField(max_length=100, null=True, blank=True)


class Admarea(models.Model):
    admarea_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class CategoryObjDict(models.Model):
    category_obj_id = models.AutoField(primary_key=True)  # ?
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Organizations(models.Model):
    inn = models.DecimalField(
        primary_key=True, max_digits=12, decimal_places=0, max_length=12
    )
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    phone_number = models.CharField(max_length=12)  # Исправить


class StatusesEvent(models.Model):
    status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Districts(models.Model):
    district_id = models.AutoField(primary_key=True)
    admarea_id = models.ForeignKey(
        Admarea, models.SET_NULL, null=True, blank=True, related_name="districts"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Favourites(models.Model):
    fav_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, models.CASCADE, related_name="favourites")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    class Meta:
        ordering = ("-pk",)


class StatusesReport(models.Model):
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


class SortPoints(models.Model):
    point_id = models.AutoField(primary_key=True)
    photo = models.ImageField(blank=True, upload_to="sort_points/", max_length=3000)
    name = models.CharField(max_length=100)
    admarea_id = models.ForeignKey(
        Admarea, models.SET_NULL, blank=True, null=True, related_name="sort_points"
    )
    district_id = ChainedForeignKey(
        Districts,
        chained_field="admarea_id",
        chained_model_field="admarea_id",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    # models.ForeignKey(Districts, models.SET_NULL, blank=True, null=True)
    transport_description = models.TextField(max_length=512)
    adress = models.CharField(max_length=256)
    locality = models.CharField(max_length=256)
    description = models.TextField(max_length=1024)
    latitude_n = models.DecimalField(max_digits=10, decimal_places=8, max_length=9)
    longitude_e = models.DecimalField(max_digits=11, decimal_places=8, max_length=9)
    organization_inn = models.ForeignKey(Organizations, models.CASCADE)
    schedule = models.CharField(max_length=100, blank=True)
    favourites = GenericRelation(Favourites)
    wast_types = models.ManyToManyField(WasteTypes)

    class Meta:
        ordering = ("-pk",)

    def __str__(self):
        return self.name


class Reports(models.Model):
    report_id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=1024)
    photo = models.ImageField(
        blank=True, upload_to="reports/", max_length=3000
    )  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True)
    status_id_r = models.ForeignKey(
        StatusesReport, models.DO_NOTHING, related_name="reports"
    )
    user_id = models.ForeignKey(CustomUser, models.CASCADE, related_name="reports")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    point_id = models.ForeignKey(
        SortPoints,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports",
    )

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Routes(models.Model):
    DIFFICULT = (
        ("A", "Очень легко"),
        ("B", "Легко"),
        ("C", "Средне"),
        ("D", "Сложно"),
    )

    route_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1024)
    start_n = models.DecimalField(max_digits=10, decimal_places=8)
    start_e = models.DecimalField(max_digits=11, decimal_places=8)
    end_n = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    end_e = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    diffictulity_level = models.CharField(max_length=1, default="A", choices=DIFFICULT)
    length = models.FloatField()
    duration = models.TextField()  # This field type is a guess.
    transport_description = models.TextField(max_length=512)
    locality = models.CharField(max_length=256)
    price = models.IntegerField()
    photo = models.ImageField(
        blank=True, upload_to="routes/", max_length=3000
    )  # This field type is a guess.
    reports = GenericRelation(Reports, related_query_name="routes")
    favourites = GenericRelation(Favourites, related_query_name="route")

    def __str__(self):
        return self.name


class NatureObjects(models.Model):
    object_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1024)
    category_obj_id = models.ForeignKey(
        CategoryObjDict,
        models.PROTECT,
        related_name="nature_objects",
    )
    latitude_n = models.DecimalField(max_digits=10, decimal_places=8, max_length=9)
    longitude_e = models.DecimalField(max_digits=11, decimal_places=8, max_length=9)
    admarea_id = models.ForeignKey(
        Admarea, models.SET_NULL, blank=True, null=True, related_name="nature_objects"
    )
    district_id = ChainedForeignKey(
        Districts,
        chained_field="admarea_id",
        chained_model_field="admarea_id",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    locality = models.CharField(max_length=256)
    transport_description = models.TextField(max_length=512)
    adress = models.CharField(max_length=256)
    organization_inn = models.ForeignKey(
        Organizations, models.SET_NULL, blank=True, null=True
    )
    has_parking = models.BooleanField(blank=True, null=True)
    photo = models.ImageField(blank=True, upload_to="nature_objects/", max_length=3000)
    schedule = models.CharField(max_length=100, blank=True)
    reports = GenericRelation(Reports, related_query_name="nature_object")
    favourites = GenericRelation(Favourites, related_query_name="place")

    class Meta:
        ordering = ("-pk",)

    def __str__(self):
        return self.name


class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1024)
    status_id = models.ForeignKey(StatusesEvent, models.PROTECT, related_name="events")
    adress = models.CharField(max_length=256)
    photo = models.ImageField(
        blank=True, upload_to="events/", max_length=3000
    )  # This field type is a guess.
    time_start = models.DateTimeField()
    time_of_close = models.DateTimeField()
    reports = GenericRelation(Reports, related_query_name="events")
    favourites = GenericRelation(Favourites)
    nature_objects = models.ManyToManyField(
        NatureObjects, blank=True, related_name="events"
    )
    routes = models.ManyToManyField(Routes, blank=True, related_name="events")

    class Meta:
        ordering = ("-pk",)

    def __str__(self):
        return self.name


class Rates(models.Model):
    rate_id = models.AutoField(primary_key=True)
    report_id = models.OneToOneField(Reports, models.CASCADE, related_name="rates")
    availability = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    beauty = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    purity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )


class Results(models.Model):
    result_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    report_id = models.ForeignKey(Reports, models.CASCADE, related_name="results")
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    waste_id = models.ForeignKey(WasteTypes, models.CASCADE, related_name="results")
    aproved = models.BooleanField(blank=True, null=True)


"""class WorkingHours(models.Model):
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
        return self.day_of_week"""
