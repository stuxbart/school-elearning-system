from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm

    list_display = ('email', 'admin')
    list_filter = ('admin', 'staff', 'admin')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'user_index')}),
        ('Courses', {'fields': ('courses',)}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'teacher', 'active')})
    )

    add_fieldsets =  (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    
    filter_horizontal = ()

admin.site.register(User, UserAdmin)