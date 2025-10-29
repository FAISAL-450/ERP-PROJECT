from django.contrib import admin
from .models import Profile, Department

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_departments')
    search_fields = ('user__username', 'user__email')
    list_filter = ('departments',)

    def get_departments(self, obj):
        return ", ".join([dept.name for dept in obj.departments.all()])
    get_departments.short_description = 'Departments'

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

