# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Patient1, Diagnosis, Notification


# Inline Profile Admin Model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Custom User Admin
class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)  # Add ProfileInline to the UserAdmin

    # Optionally customize list display for users in the admin interface
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')

    # You can also filter by role here if you like
    list_filter = ('is_active', 'is_staff', 'profile__role')


# Unregister the default UserAdmin and register the custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Register Profile Model separately (if you need to access profiles directly)
admin.site.register(Profile)

admin.site.register(Patient1)
admin.site.register(Diagnosis)
admin.site.register(Notification)
