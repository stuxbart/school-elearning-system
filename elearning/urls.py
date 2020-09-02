"""elearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import home_view

api_urlpatterns = [
    path('courses/', include('courses.api.urls.course')),
    path('modules/', include('courses.api.urls.module')),
    path('categories/', include('courses.api.urls.category')),
    path('users/', include('accounts.api.urls.users')),
    path('auth/', include('accounts.api.urls.auth'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls', 'accounts')),
    path('courses/', include('courses.urls', 'courses')),
    path('search/', include('search.urls', 'search')),

    path('api/', include(api_urlpatterns))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
