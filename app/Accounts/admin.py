from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import ProfileImage
from .forms import CustomUserChangeForm,CustomUserCreationForm

CustomUser=get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form=CustomUserCreationForm
    form=CustomUserChangeForm
    model=CustomUser
    ordering = ('username',)
    add_fieldsets = (('information',{'fields':('username','password1', 'password2','first_name','last_name','date_of_birth', 'address', 'mobile_no', 'role', 'status', 'designation', 'approved_by'),},),('Advanced options',{'classes':('collapse',),'fields': ('is_superuser',)},),)
    fieldsets=(('information',{'fields':('username','first_name','last_name','gender','date_of_birth', 'address', 'mobile_no', 'status', 'role', 'designation', 'approved_by'),},),('Advanced options',{'classes':('collapse',),'fields': ('is_superuser',)},),)
    list_display=['username','first_name','last_name']
    search_fields = ('username',)



admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(ProfileImage)