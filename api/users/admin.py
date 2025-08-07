from django.contrib import admin
from .models import User

@admin.register(User)
class UseraAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username', 'email')
