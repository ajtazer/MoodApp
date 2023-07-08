from django.urls import path, include, re_path
from django.views.static import serve
from django.contrib import admin
from django.conf import settings
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='Home Page'),
    path('signin/', views.signin, name='Login Page'),
    path('signup/', views.signup, name='Register Page'),
    path('logout/', views.logout, name='Logout Request'),
    path('accounts/', include('allauth.urls')),
    path('social/',include ('social.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
admin.site.site_header = settings.ADMIN_SITE_HEADER