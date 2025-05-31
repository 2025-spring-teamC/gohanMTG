from django.contrib import admin
from search.models import Recipe, Group_recipe, User_recipe

@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('user', 'url', 'created_at', 'updated_at')
    search_fields = ('user',)


@admin.register(Group_recipe)
class GroupRecipesAdmin(admin.ModelAdmin):
    list_display = ('group', 'recipe', 'user', 'created_at')
    list_filter = ('group', 'user')
    search_fields = ('group__name', 'recipe__name', 'user__name')


@admin.register(User_recipe)
class UserRecipesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__name', 'recipe__name')