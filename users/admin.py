from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    model = User

#: Register User model to admin site

admin.site.register(User, UserAdmin)