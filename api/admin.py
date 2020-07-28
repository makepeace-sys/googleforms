# Django
from django.contrib import admin

# Models
from api.models import User, Form


class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name', 'email', 'is_admin', 'is_verify')
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_admin', 'is_verify')
    list_filter = ('is_active', 'is_admin', 'is_verify')
    search_fields = ('username', 'first_name', 'last_name')


admin.site.register(User)


# class FormAdmin(admin.ModelAdmin):
#     fields = ('name', 'description', 'is_active')
#     list_display = ('name', 'description', 'is_active')
#     search_fields = 'is_active'
#
#
# admin.site.register(Form, FormAdmin)
