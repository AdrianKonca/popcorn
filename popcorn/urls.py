"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from django_registration.backends.activation.views import RegistrationView
from django.contrib.auth import views as auth_views

from . import views
from .forms import UserRegistrationForm

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/add/', views.edit_recipe, name='add_recipe'),
    path('recipes/edit/<str:slug>', views.edit_recipe, name='edit_recipe'),
    path('recipes/view/<str:slug>', views.post_comment, name='recipe'),
    path('recipes/view/<str:slug>/vote', views.vote_recipe, name='vote_recipe'),  # used on front-end
    path('comments/vote/<int:pk>', views.vote_comment, name='vote_comment'),  # used on front-end
    path('categories/', views.CategoriesView.as_view(), name='categories'),

    path('accounts/profile/', views.userpage, name='user_page'),
    path('accounts/register/',
         RegistrationView.as_view(
             form_class=UserRegistrationForm
         ),
         name='django_registration_register',
         ),
    path('accounts/',
         include('django_registration.backends.activation.urls')
         ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_view, name='logout'),
]
