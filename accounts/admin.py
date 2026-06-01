from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, JobSeekerProfile, CompanyProfile, ContactMessage

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'date_joined']
    list_filter = ['user_type']
    fieldsets = UserAdmin.fieldsets + (('Type', {'fields': ('user_type',)}),)

admin.site.register(JobSeekerProfile)
admin.site.register(CompanyProfile)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    list_per_page = 20
