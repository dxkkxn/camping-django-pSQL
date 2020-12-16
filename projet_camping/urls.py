"""projet_camping URL Configuration

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
from django.contrib import admin
from django.urls import path
from camping.views import (register_create_view, login_create_view,
                            home_create_view, profile_create_view,
                            services_create_view, reservation_create_view,
                            resv_annulation_view, login_admin_create_view,
                            admin_create_view)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_create_view),
    path('register/', register_create_view),
    path('profile/', profile_create_view),
    path('services/', services_create_view),
    path('reservation/', reservation_create_view),
    path('resv-annulation/', resv_annulation_view),
    path('login/admin/',login_admin_create_view),
    path('camping/admin/', admin_create_view),
    path('', home_create_view)
]
