# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Districts(models.Model):
    districtid = models.OneToOneField('Objects', models.DO_NOTHING, db_column='districtID', primary_key=True)  # Field name made lowercase.
    admareaid = models.OneToOneField('Admarea', models.DO_NOTHING, db_column='admareaID')  # Field name made lowercase.
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'Districts'


class Events(models.Model):
    eventid = models.AutoField(db_column='EventID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    statusid = models.OneToOneField('Statuses', models.DO_NOTHING, db_column='StatusID')  # Field name made lowercase.
    adress = models.CharField(max_length=256)
    latitude_n = models.DecimalField(db_column='latitude_N', max_digits=8, decimal_places=6, max_length=9)  # Field name made lowercase.
    longitude_e = models.DecimalField(db_column='longitude_E', max_digits=8, decimal_places=6, max_length=9)  # Field name made lowercase.
    photo = models.ImageField(blank=True, null=True)  # This field type is a guess.
    time = models.DateTimeField()
    time_of_close = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Events'


class Favourites(models.Model):
    favid = models.AutoField(db_column='FavID', primary_key=True)  # Field name made lowercase.
    userid = models.OneToOneField('Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    eventid = models.OneToOneField('Events', models.DO_NOTHING, db_column='EventID', blank=True, null=True)  # Field name made lowercase.
    objectid = models.OneToOneField('Objects', models.DO_NOTHING, db_column='ObjectID', blank=True, null=True)  # Field name made lowercase.
    routeid = models.OneToOneField('Route', models.DO_NOTHING, db_column='RouteID', blank=True, null=True)  # Field name made lowercase.
    pointid = models.OneToOneField('GarbagePoints', models.DO_NOTHING, db_column='PointID', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.favid

    class Meta:
        managed = False
        db_table = 'Favourites'


class GarbagePoints(models.Model):
    pointid = models.AutoField(db_column='PointID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=64)
    admareaid = models.OneToOneField('Admarea', models.DO_NOTHING, db_column='admareaID', blank=True, null=True)  # Field name made lowercase.
    districtid = models.OneToOneField('Districts', models.DO_NOTHING, db_column='districtID', blank=True, null=True)  # Field name made lowercase.
    transport = models.CharField(max_length=100)
    adress = models.CharField(max_length=256)
    locality = models.CharField(max_length=256)
    description = models.CharField(max_length=100)
    latitude_n = models.DecimalField(db_column='latitude_N', max_digits=8, decimal_places=6, max_length=9)  # Field name made lowercase.
    longitude_e = models.DecimalField(db_column='longitude_E', max_digits=8, decimal_places=5, max_length=9)  # Field name made lowercase.
    working_hoursid = models.OneToOneField('WorkingHours', models.DO_NOTHING, db_column='working_hoursID')  # Field name made lowercase.
    organization_inn = models.OneToOneField('Organizations', models.DO_NOTHING, unique=True, db_column='organization_inn')

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Garbage_points'
        unique_together = (('pointid', 'working_hoursid', 'organization_inn'),)


class Objects(models.Model):
    objectid = models.AutoField(db_column='ObjectID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    category_obj_id = models.OneToOneField('CategoryObjDic', models.DO_NOTHING, db_column='category_obj_ID')  # Field name made lowercase.
    latitude_n = models.DecimalField(db_column='latitude_N', max_digits=8, decimal_places=6, max_length=9)  # Field name made lowercase.
    longitude_e = models.DecimalField(db_column='longitude_E', max_digits=8, decimal_places=6, max_length=9)  # Field name made lowercase.
    locality = models.CharField(max_length=256)
    transport = models.CharField(max_length=100)
    adress = models.CharField(max_length=256)
    organization_inn = models.OneToOneField('Organizations', models.DO_NOTHING, db_column='organization_inn', blank=True, null=True)
    working_hoursid = models.OneToOneField('WorkingHours', models.DO_NOTHING, db_column='working_hoursID', blank=True, null=True)  # Field name made lowercase.
    has_parking = models.BooleanField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    admareaid = models.ForeignKey('Admarea', models.DO_NOTHING, db_column='admareaID', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Objects'


class Organizations(models.Model):
    organization_inn = models.DecimalField(primary_key=True, max_digits=12, decimal_places=0, max_length=12)
    name = models.CharField(max_length=64)
    e_mail = models.CharField(db_column='e-mail', max_length=64)  # Field renamed to remove unsuitable characters.
    phone = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'Organizations'


class Rates(models.Model):
    estimation = {
        ('A', '1'),
        ('B', '2'),
        ('C', '3'),
        ('D', '4'),
        ('E', '5')
    }

    rateid = models.AutoField(db_column='RateID', primary_key=True)  # Field name made lowercase.
    reportid = models.ForeignKey('Reports', models.DO_NOTHING, db_column='ReportID')  # Field name made lowercase.
    rate1 = models.CharField(db_column='Rate1', max_length=1, default='A', choices=estimation)  # Field name made lowercase.
    rate2 = models.CharField(db_column='Rate2', max_length=1, default='B', choices=estimation)  # Field name made lowercase.
    rate3 = models.CharField(db_column='Rate3', max_length=1, default='C', choices=estimation)  # Field name made lowercase.

    def __str__(self):
        return self.rateid

    class Meta:
        managed = False
        db_table = 'Rates'


class Reports(models.Model):
    reportid = models.AutoField(db_column='ReportID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(max_length=100)
    photo = models.ImageField(blank=True, null=True)  # This field type is a guess.
    time = models.DateTimeField()
    statusid_r = models.ForeignKey('StatusesR', models.DO_NOTHING, db_column='StatusID_R')  # Field name made lowercase.
    eventid = models.ForeignKey(Events, models.DO_NOTHING, db_column='EventID', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    routeid = models.ForeignKey('Route', models.DO_NOTHING, db_column='RouteID', blank=True, null=True)  # Field name made lowercase.
    pointid = models.ForeignKey('GarbagePoints', models.DO_NOTHING, db_column='PointID', blank=True, null=True)  # Field name made lowercase.
    objectid = models.ForeignKey('Objects', models.DO_NOTHING, db_column='ObjectID', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.reportid

    class Meta:
        managed = False
        db_table = 'Reports'


class ReportsEvents(models.Model):
    reports_events_id = models.AutoField(db_column='Reports_Events_Id', primary_key=True)  # Field name made lowercase.
    reports_reportid = models.OneToOneField('Reports', models.DO_NOTHING, db_column='Reports_ReportID')  # Field name made lowercase.
    events_reportid = models.OneToOneField('Events', models.DO_NOTHING, db_column='Events_ReportID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Reports_Events'


class Results(models.Model):
    resultid = models.AutoField(db_column='ResultID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(max_length=100)
    time = models.DateTimeField()
    amount = models.DecimalField(max_digits=65535, decimal_places=65535)
    wasteid = models.OneToOneField('WasteTypes', models.DO_NOTHING, db_column='WasteID')  # Field name made lowercase.
    aproved = models.BooleanField(blank=True, null=True)
    reportid = models.ForeignKey(Reports, models.DO_NOTHING, db_column='ReportID', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.resultid

    class Meta:
        managed = False
        db_table = 'Results'


class Roles(models.Model):
    roleid = models.AutoField(db_column='RoleID', primary_key=True)  # Field name made lowercase.
    role_name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'Roles'


# class Routes(models.Model):
#     difficult = {
#         ('A', 'Очень легко'),
#         ('B', 'Легко'),
#         ('C', 'Средне'),
#         ('D', 'Сложно')
#     }
#
#     routeid = models.AutoField(db_column='RouteID', primary_key=True)  # Field name made lowercase.
#     name = models.CharField(max_length=64)
#     description = models.CharField(max_length=100)
#     start_n = models.DecimalField(db_column='start_N', max_digits=8, decimal_places=6)  # Field name made lowercase.
#     start_e = models.DecimalField(db_column='start_E', max_digits=7, decimal_places=5)  # Field name made lowercase.
#     end_n = models.DecimalField(db_column='end_N', max_digits=8, decimal_places=6)  # Field name made lowercase.
#     end_e = models.DecimalField(db_column='end_E', max_digits=7, decimal_places=5)  # Field name made lowercase.
#     diffictulityid = models.CharField(db_column='diffictulityID', max_length=20, default='A', choices=difficult)  # Field name made lowercase.
#     lenght = models.FloatField()
#     duration = models.TextField()  # This field type is a guess.
#     transport = models.CharField(max_length=100)
#     locality = models.CharField(max_length=256)
#     price = models.IntegerField(blank=True, null=True)
#     photo = models.ImageField(blank=True, null=True)  # This field type is a guess.
#
#     class Meta:
#         managed = False
#         db_table = 'Routes'
#

class SexDic(models.Model):
    sexid = models.AutoField(db_column='SexID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Sex_dic'


class Users(models.Model):
    sex = {
        ('M', 'Мужской'),
        ('W', 'Женский')
    }
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=32)
    publicname = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    birth_date = models.DateTimeField()
    locality = models.CharField(max_length=256)
    photo = models.ImageField(blank=True, null=True)  # This field type is a guess.
    sexid = models.CharField(db_column='SexID', max_length=10, default='M', choices=sex)  # Field name made lowercase.
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    created_at = models.DateTimeField()
    active = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Users'


class WasteTypes(models.Model):
    wasteid = models.AutoField(db_column='WasteID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Waste_types'


class Admarea(models.Model):
    admareaid = models.AutoField(db_column='admareaID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'admarea'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Difictulites(models.Model):
    diffictulityid = models.AutoField(db_column='diffictulityID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'difictulites'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EventsOnObjects(models.Model):
    eventid = models.OneToOneField(Events, models.DO_NOTHING, db_column='EventID')  # Field name made lowercase.
    objectid = models.OneToOneField(Objects, models.DO_NOTHING, db_column='ObjectID')  # Field name made lowercase.
    eo_id = models.AutoField(db_column='EO_ID', primary_key=True)  # Field name made lowercase.

    def __str__(self):
        return self.eo_id

    class Meta:
        managed = False
        db_table = 'events_on_objects'


class EventsOnRoutes(models.Model):
    eventid = models.OneToOneField(Events, models.DO_NOTHING, db_column='EventID', primary_key=True)  # Field name made lowercase.
    routeid = models.OneToOneField('Route', models.DO_NOTHING, db_column='RouteID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'events_on_routes'
        unique_together = (('eventid', 'routeid'),)


class Permission(models.Model):
    permission_id = models.AutoField(db_column='Permission_ID', primary_key=True)  # Field name made lowercase.
    name_of_premission = models.TextField(db_column='name_of premission', db_collation='C')  # Field renamed to remove unsuitable characters. This field type is a guess.
    valid = models.BooleanField()

    def __str__(self):
        return self.name_of_premission

    class Meta:
        managed = False
        db_table = 'permission'


class PointTypes(models.Model):
    wasteid = models.OneToOneField('WasteTypes', models.DO_NOTHING, db_column='WasteID', primary_key=True)  # Field name made lowercase.
    pointid = models.OneToOneField('GarbagePoints',  models.DO_NOTHING, db_column='PointID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'point_types'
        unique_together = (('wasteid', 'pointid'),)


class RoleOnPermission(models.Model):
    roleid = models.OneToOneField('Roles', models.DO_NOTHING, db_column='RoleID', primary_key=True)  # Field name made lowercase.
    permissionid = models.OneToOneField('Permission', models.DO_NOTHING, db_column='PermissionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'role_on_permission'
        unique_together = (('roleid', 'permissionid'),)


class Route(models.Model):
    difficult = {
        ('A', 'Очень легко'),
        ('B', 'Легко'),
        ('C', 'Средне'),
        ('D', 'Сложно')
            }
    route_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    start_n = models.DecimalField(db_column='start_N', max_digits=8, decimal_places=6)  # Field name made lowercase.
    start_e = models.DecimalField(db_column='start_E', max_digits=7, decimal_places=5)  # Field name made lowercase.
    end_n = models.DecimalField(db_column='end_N', max_digits=8, decimal_places=6)  # Field name made lowercase.
    end_e = models.DecimalField(db_column='end_E', max_digits=7, decimal_places=5)  # Field name made lowercase.
    diffictulityid = models.CharField(db_column='diffictulityID', max_length=20, default='A', choices=difficult)  # Field name made lowercase.
    lenght = models.FloatField()
    duration = models.TextField()  # This field type is a guess.
    transport = models.CharField(max_length=100)
    locality = models.CharField(max_length=256)
    price = models.IntegerField()
    photo = models.ImageField(blank=True, null=True)  # This field type is a guess.

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'route'


class Statuses(models.Model):
    statusid = models.AutoField(db_column='statusID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'statuses'


class StatusesR(models.Model):
    statusid_r = models.AutoField(db_column='StatusID_R', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'statuses_r'


class UserHasRole(models.Model):
    userid = models.OneToOneField('Users', models.DO_NOTHING, db_column='UserID', primary_key=True)  # Field name made lowercase.
    roleid = models.OneToOneField('Roles', models.DO_NOTHING, db_column='RoleID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_has_role'
        unique_together = (('userid', 'roleid'),)


class WorkingHours(models.Model):
    workin_hoursid = models.AutoField(db_column='workin_hoursID', primary_key=True)  # Field name made lowercase.
    day_of_week = models.CharField(max_length=32)
    open_time = models.TimeField()
    close_time = models.TimeField()
    each = models.CharField(max_length=32)

    def __str__(self):
        return self.workin_hoursid

    class Meta:
        managed = False
        db_table = 'working_hours'


class CategoryObjDic(models.Model):
    category_obj_dic = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'category_obj_dic'
