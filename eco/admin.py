from django.contrib import admin
from .models import *


@admin.register(Districts)
class CategoryDistricts(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(Events)
class CategoryEvents(admin.ModelAdmin):
    list_display = ('name', 'event_id')
    filter_horizontal = ('nature_objects', 'routes')


@admin.register(Favourites)
class CategoryFavourites(admin.ModelAdmin):
    list_display = ('fav_id',)


@admin.register(SortPoints)
class CategoryGarbagePoints(admin.ModelAdmin):
    list_display = ('point_id', 'name')
    filter_horizontal = ('wast_types',)


@admin.register(NatureObjects)
class CategoryObjects(admin.ModelAdmin):
    list_display = ('object_id', 'name')


@admin.register(Organizations)
class CategoryOrganizations(admin.ModelAdmin):
    list_display = ('inn', 'name')


@admin.register(Rates)
class CategoryRates(admin.ModelAdmin):
    list_display = ('rate_id',)


@admin.register(Reports)
class CategoryReports(admin.ModelAdmin):
    list_display = ('report_id', 'description')


@admin.register(Results)
class CategoryResults(admin.ModelAdmin):
    list_display = ('result_id',)


@admin.register(Routes)
class CategoryRoute(admin.ModelAdmin):
    list_display = ('route_id', 'name')


@admin.register(WasteTypes)
class CategoryWasteTypes(admin.ModelAdmin):
    list_display = ('waste_id', 'name')


@admin.register(Admarea)
class CategoryAdmarea(admin.ModelAdmin):
    list_display = ('admarea_id', 'name')

@admin.register(StatusesDict)
class CategoryStatuses(admin.ModelAdmin):
    list_display = ('status_id', 'name')


@admin.register(StatusesRDict)
class CategoryStatusesR(admin.ModelAdmin):
    list_display = ('status_id_r', 'name')


@admin.register(CategoryObjDict)
class CategoryCategoryObjDic(admin.ModelAdmin):
    list_display = ('category_obj_id', 'name')

