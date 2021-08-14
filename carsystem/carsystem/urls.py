"""carsystem URL Configuration

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
from carsystem.settings import MEDIA_ROOT
from django.conf.urls import url, include
from django.views.static import serve
from carweb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^',include('carweb.urls')),
    path('login/', views.login),
    path('carshow/', views.carshow),
    path('carshow/<num>',views.carshow),
    path('cardetails/<carid>',views.cardetails),
    path('index/',views.index),
    path('predict/',views.predict),
    path('predict1/',views.predict1),
    path('login1/',views.login1),
    path('userroom/',views.userroom),
    path('popularcar/',views.popularcar),
    path('sale/',views.sale),
]
