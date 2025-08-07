from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')

@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'team', 'created_at', 'updated_at')