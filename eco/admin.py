from django.contrib import admin
from .models import *


@admin.register(Districts)
class CategoryDistricts(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(Events)
class CategoryEvents(admin.ModelAdmin):
    list_display = ('name', 'eventid')


@admin.register(Favourites)
class CategoryFavourites(admin.ModelAdmin):
    list_display = ('favid',)


@admin.register(GarbagePoints)
class CategoryGarbagePoints(admin.ModelAdmin):
    list_display = ('pointid', 'name')


@admin.register(Objects)
class CategoryObjects(admin.ModelAdmin):
    list_display = ('objectid', 'name')


@admin.register(Organizations)
class CategoryOrganizations(admin.ModelAdmin):
    list_display = ('organization_inn', 'name')


@admin.register(Rates)
class CategoryRates(admin.ModelAdmin):
    list_display = ('rateid',)


@admin.register(Reports)
class CategoryReports(admin.ModelAdmin):
    list_display = ('reportid', 'description')


@admin.register(Results)
class CategoryResults(admin.ModelAdmin):
    list_display = ('resultid', 'description')


@admin.register(Roles)
class CategoryRoles(admin.ModelAdmin):
    list_display = ('roleid', 'role_name')


@admin.register(Route)
class CategoryRoute(admin.ModelAdmin):
    list_display = ('route_id', 'name')


@admin.register(SexDic)
class CategorySexDic(admin.ModelAdmin):
    list_display = ('sexid', 'name')


@admin.register(Users)
class CategoryUsers(admin.ModelAdmin):
    list_display = ('userid', 'name')


@admin.register(WasteTypes)
class CategoryWasteTypes(admin.ModelAdmin):
    list_display = ('wasteid', 'name')


@admin.register(Admarea)
class CategoryAdmarea(admin.ModelAdmin):
    list_display = ('admareaid', 'name')


@admin.register(ReportsEvents)
class CategoryReportsEvents(admin.ModelAdmin):
    list_display = ('reports_reportid',)


@admin.register(Difictulites)
class CategoryDifictulites(admin.ModelAdmin):
    list_display = ('diffictulityid', 'name')


@admin.register(EventsOnObjects)
class CategoryEventsOnObjects(admin.ModelAdmin):
    list_display = ('eo_id',)


@admin.register(EventsOnRoutes)
class CategoryEventsOnRoutes(admin.ModelAdmin):
    list_display = ('eventid',)


@admin.register(Permission)
class CategoryPermission(admin.ModelAdmin):
    list_display = ('permission_id', 'name_of_premission')


@admin.register(PointTypes)
class CategoryPointTypes(admin.ModelAdmin):
    list_display = ('wasteid',)


@admin.register(Statuses)
class CategoryStatuses(admin.ModelAdmin):
    list_display = ('statusid', 'name')


@admin.register(StatusesR)
class CategoryStatusesR(admin.ModelAdmin):
    list_display = ('statusid_r', 'name')


@admin.register(WorkingHours)
class CategoryWorkingHours(admin.ModelAdmin):
    list_display = ('workin_hoursid', 'day_of_week')


@admin.register(CategoryObjDic)
class CategoryCategoryObjDic(admin.ModelAdmin):
    list_display = ('category_obj_dic', 'name')


admin.site.register(RoleOnPermission)
admin.site.register(UserHasRole)
# admin.site.register(AuthGroupPermissions)
# admin.site.register(AuthPermission)
# admin.site.register(AuthUser)
# admin.site.register(AuthUserGroups)
# admin.site.register(AuthUserUserPermissions)
# admin.site.register(DjangoAdminLog)
# admin.site.register(DjangoContentType)
# admin.site.register(DjangoMigrations)
# admin.site.register(DjangoSession)
# Register your models here.
