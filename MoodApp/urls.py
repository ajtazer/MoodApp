from django.urls import path, include, re_path
from django.views.static import serve
from django.contrib import admin
from django.conf import settings
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='Home Page'),
    path('feed/', views.feed, name='Feeds Page'),
    path('upload/', views.upload, name='Upload Request'),
    path('signin/', views.signin, name='Login Page'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='Register Page'),
    path('logout/', views.logout, name='Logout Request'),
    path('explore/', views.explore, name='Explore Page'),
    path('post/<uuid:post_id>/', views.post_detail, name='Post Detail'),
    path('post/<uuid:post_id>/like/', views.like_post, name='Like Post'),
    path('post/<uuid:post_id>/comment/', views.add_comment, name='Add Comment'),
    path('accounts/', include('allauth.urls')),
    path('social/',include ('social.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
admin.site.site_header = settings.ADMIN_SITE_HEADER
