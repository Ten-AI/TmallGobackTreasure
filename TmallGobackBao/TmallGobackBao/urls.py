"""TmallGobackBao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from tmall import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('login/merchant/', views.login),
    path('login/yunying/', views.login_as_yunying),
    path('base/', views.IndexView.as_view(), name='test'),
    path('base2/', views.IndexView2.as_view(), name='test'),
    path('roi/<str:min>/<str:max>/', views.ChartView3.as_view(), name='test'),
    path('charts/<str:charts_type>/', views.ChartView.as_view(), name='test'),
    path('charts_yunying/<str:charts_type>/', views.ChartView2.as_view(), name='test'),
    # path('charts/gmv/', views.ChartGmv.as_view(), name='test'),

]
