from django.urls import path

from . import views

urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    path('chart', views.chartPage, name='chartPage'),
    path('uploadexcel', views.uploadExcel, name='uploadexcel'),
]