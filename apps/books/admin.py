from django.contrib import admin
from .models import Category, Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publication_year')
    list_filter = ('category', 'publication_year', 'language')
    search_fields = ('title', 'author__name', 'isbn')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('author', 'category')
