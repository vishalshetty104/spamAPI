from django.contrib import admin
from .models import User,GlobalDb
# Register your models here.

@admin.register(User) #displays all registered users
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(GlobalDb) #displays contents of global database
class GlobalDb(admin.ModelAdmin):
    pass