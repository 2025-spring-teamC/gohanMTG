from django.db import models
from django.utils import timezone
from account.models import FamilyGroup, User


#レシピのデータ抜き出し保存用
#Recipesテーブルの設定
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes_links")
    url = models.URLField(verbose_name="レシピURL", max_length=1000, null=False)
    created_at = models.DateTimeField(verbose_name="登録日", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        db_table = 'Recipes'

    def __str__(self):
        return self.url


#グループの食べたいレシピ
#Group_recipesテーブルの設定
class Group_recipe(models.Model):
    group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name="group_recipes_links")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="group_recipes_links")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_recipes_links")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Group_recipes'

    def __str__(self):
        return f"{self.group.name} - {self.recipe.url} - {self.user.name}"


#ユーザーのお気に入りレシピ
#User_recipesテーブルの設定
class User_recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_recipes_links")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="user_recipes_links")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'User_recipes'

    def __str__(self):
        return f"{self.user.name} - {self.recipe.url}"
