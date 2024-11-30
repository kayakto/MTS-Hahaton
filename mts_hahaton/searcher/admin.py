from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *


@admin.register(Unit)
class UnitAdmin(MPTTModelAdmin):
    list_display = ('name', 'unit_type', 'parent')
    list_filter = ('unit_type',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_role')
    list_filter = ('employee_role',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'position', 'city', 'email', 'phone')
    list_filter = ('unit', 'position', 'city')
    search_fields = ('name', 'first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')
    autocomplete_fields = ('unit', 'position')
