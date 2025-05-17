from django.contrib import admin
from .models import User, Contact, Media, Blog, Project, Donation, OurWork, Admin_profile, Task,Emp_Profile,Vol_Profile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'role')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'file', 'uploaded_at')
    list_filter = ('media_type',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published')
    list_filter = ('published',)
    search_fields = ('title', 'author__username')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'is_anonymous', 'created_at')
    list_filter = ('is_anonymous',)
    search_fields = ('user__username',)

@admin.register(OurWork)
class OurWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

@admin.register(Admin_profile)
class Admin_profileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'gender', 'mobile_number', 'email')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'completed', 'created_at')
    list_filter = ('completed',)
    search_fields = ('title', 'assigned_to__username')

@admin.register(Emp_Profile)
class Emp_ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'gender', 'mobile_number', 'email')

@admin.register(Vol_Profile)
class Vol_ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'gender', 'mobile_number', 'email')
    