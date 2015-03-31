from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from ppuser.models import CustomUser
from ppuser.forms import CustomUserChangeForm, CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('username', 'display_name', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 
            'verified_on')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'display_name', 'first_name', 'last_name', 
                'email', 'password1', 'password2')}
        ),
    )

    form        = CustomUserChangeForm
    add_form    = CustomUserCreationForm

    list_display = ('username', 'display_name', 'email', 'first_name', 
        'last_name', 'is_staff')
    search_fields = ('username', 'display_name', 'email', 'first_name', 
        'last_name')
    ordering = ('username','display_name',)

admin.site.register(get_user_model(), CustomUserAdmin)
