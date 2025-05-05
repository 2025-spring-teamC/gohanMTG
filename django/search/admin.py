from django.contrib import admin
from search.models import Recipes, Group_recipes, User_recipes

@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_id', 'url', 'created_at', 'updated_at')
    search_fields = ('name', 'category_id')


@admin.register(Group_recipes)
class GroupRecipesAdmin(admin.ModelAdmin):
    list_display = ('group', 'recipe', 'user', 'created_at')
    list_filter = ('group', 'user')
    search_fields = ('group__name', 'recipe__name', 'user__name')


@admin.register(User_recipes)
class UserRecipesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__name', 'recipe__name')