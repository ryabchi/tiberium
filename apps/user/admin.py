from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import SystemUserData, UserProfile


class UserProfileInline(admin.StackedInline):
    def view_uuid(self, obj):
        return obj.id

    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User profile'
    list_display = ['view_uuid', 'role', 'is_system', 'login', 'name', 'updated_at', 'created_at', 'is_active']
    readonly_fields = ['view_uuid', 'updated_at', 'created_at']


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class SystemUserDataForm(ModelForm):
    class Meta:
        model = SystemUserData
        fields = '__all__'


class SystemUserDataFormAdmin(admin.ModelAdmin):
    form = SystemUserDataForm
    list_display = ['profile', 'password']


admin.site.register(SystemUserData, SystemUserDataFormAdmin)
