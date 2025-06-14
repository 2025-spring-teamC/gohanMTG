"""
URL configuration for gohanMTG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account import views
from search.views import wantToEat_view, searchRecipes_view,recipeDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path("group-select/", views.group_select_view, name="group_select"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("", wantToEat_view, name="want_to_eat"),
    path('search_recipes/', searchRecipes_view, name='search_recipes'),
    path('detail_recipes/<int:recipe_id>/', recipeDetail, name='recipe_detail'),
    path("health/", views.health_check, name="health"),
]
