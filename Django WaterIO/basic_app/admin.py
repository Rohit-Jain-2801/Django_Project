from django.contrib import admin
from basic_app.models import UserProfileInfo,City

class UserProfileInfoAdmin(admin.ModelAdmin):
    # fields = ['profile_pic','user']
    search_fields = ['profile_pic']
    # list_filter = ['user']
    list_display = ['user','profile_pic']

class CityAdmin(admin.ModelAdmin):
    # fields = ['profile_pic','user']
    search_fields = ['user']
    # list_filter = ['user']
    list_display = ['name','user']

# Register your models here.
admin.site.register(UserProfileInfo,UserProfileInfoAdmin)
admin.site.register(City,CityAdmin)
