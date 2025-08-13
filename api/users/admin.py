from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UseraAdmin(UserAdmin):
    fieldsets= (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
      (None, {
          'classes': ('wide', ),
          'fields': ('username', 'first_name', 'last_name', 'email', 'groups', 'password1', 'password2'),
      }),
    )
    list_display = ('id', 'full_name', 'username', 'email', 'phone')
    search_fields = ['id', 'first_name', 'last_name', 'username', 'email', 'phone']
    ordering = ('-id',)
    