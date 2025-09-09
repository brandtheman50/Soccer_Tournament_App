from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ['name']
    ordering = ('name',)

@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'team', 'role', 'status', 'joined_at', 'updated_at')
    search_fields = ['user__first_name', 'user__last_name', 'team__name', 'id']
    ordering = ('-id',)