from django.contrib import admin
from .models import Manuscript

@admin.register(Manuscript)
class ManuscriptAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'author_name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
