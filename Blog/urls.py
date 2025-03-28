from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('api/', include('posts.urls')),

    #FOR FRONTEND PART
    # path('', views.index, name='index'),
    # path('login-page', views.login_page, name='login-page'),
    # path('register-page', views.register_page, name='register-page'),
    # path('create-post', views.create_post, name='create-post'),
]


if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)