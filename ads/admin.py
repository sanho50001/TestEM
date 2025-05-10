from django.contrib import admin
from .models import Category, Item, ExchangeProposal, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'condition', 'created_at', 'is_active')
    list_filter = ('category', 'condition', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    date_hierarchy = 'created_at'

@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('offered_item', 'desired_item', 'sender', 'receiver', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('offered_item__title', 'desired_item__title', 'sender__username', 'receiver__username')
    date_hierarchy = 'created_at'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'rating', 'created_at')
    search_fields = ('user__username', 'phone', 'address')
    date_hierarchy = 'created_at'
