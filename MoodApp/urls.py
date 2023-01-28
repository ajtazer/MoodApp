from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='Home Page'),
    path('signin/', views.signin, name='Login Page'),
    path('signup/', views.signup, name='Register Page'),
    path('logout/', views.logout, name='Logout Request'),
    path('accounts/', include('allauth.urls')),
    # path('accounts/', include("django.contrib.auth")),
    path('social/',include ('social.urls')),
]