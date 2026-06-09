from django.contrib import admin
from .models import Profile, StartupPost, Connection, Message, ContactReveal

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'industry', 'city', 'verified', 'premium')
    list_filter = ('role', 'industry', 'verified', 'premium')
    search_fields = ('full_name', 'company_name', 'industry', 'city')

@admin.register(StartupPost)
class StartupPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    search_fields = ('title', 'content', 'category')

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    list_filter = ('status',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'created_at', 'is_read')

@admin.register(ContactReveal)
class ContactRevealAdmin(admin.ModelAdmin):
    list_display = ('viewer', 'target', 'ip_address', 'revealed_at')
