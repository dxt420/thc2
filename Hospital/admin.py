from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from . forms import CustomUserCreationForm
from . models import CustomUser,Patient,Department,Doctor,PaymentHistory,BedAllotment



# Register your models here.

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['email','username']
    


# admin.site.register(CustomUser,CustomUserAdmin)

# admin.site.register(Patient)
# admin.site.register(Department)
# admin.site.register(Doctor)
# admin.site.register(PaymentHistory)
# admin.site.register(BedAllotment)


