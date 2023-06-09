from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

# Register your models here.


class CustomUserAdmin(UserAdmin):
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm
    model = Custom_User
    list_display = ['email', 'is_staff', "is_admin"]
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'phone_number', 'country')}),
        # ('Personal info', {'fields': ()}),
        # ('Permissions', {'fields': ('admin',)}),
    )
    search_fields = ['email']
    ordering = ['email']


admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Custom_User)
