from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserResetToken
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'full_name', 'username', 'phone', 'email', 'is_superuser', 'is_staff', 'is_active', 'is_verified', 'created_at')
    readonly_fields = ('last_login', 'modified_at', 'created_at')
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'is_verified')
    date_hierarchy = 'created_at'
    ordering = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('last_name', 'first_name', 'middle_name', 'phone', 'email')}),
        (_('Permissions'), {'fields': (('is_superuser', 'is_staff', 'is_active', 'is_verified'), 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login', 'modified_at', 'created_at')}),
    )
    add_fieldsets = (
        ('Creating a new user', {'classes': ('wide',), 'fields': ('username', 'password1', 'password2'), }),
    )
    search_fields = ('phone', 'first_name', 'last_name', 'middle_name', 'username', 'email')


class UserResetTokenAdmin(admin.ModelAdmin):
    search_fields = ('message_id', 'user__phone', 'user__first_name', 'user__last_name')
    list_display = ('id', 'message_id', 'full_name', 'phone', 'expire_date', 'is_used', 'modified_at', 'created_at')
    readonly_fields = ('message_id', 'user', 'content', 'expire_date', 'is_used', 'modified_at', 'created_at')
    date_hierarchy = 'created_at'
    list_filter = ('is_used', )


admin.site.register(User, UserAdmin)
admin.site.register(UserResetToken, UserResetTokenAdmin)

