from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Category, Product
# Register your models here.

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
	list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'update']
	list_filter = ['available', 'created', 'update']
	list_editable = ['price', 'stock']
	prepopulated_fields = {'slug': ('name',)}
