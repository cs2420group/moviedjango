from django.contrib import admin
from .models import Item, Review

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date') 
    search_fields = ('title',) 

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('item', 'author', 'rating')
    list_filter = ('rating',)
    

