from django.urls import path
from . import views

urlpatterns = [
    path('', views.monitor_procesos, name='monitor_procesos'),
    path('terminar_proceso/', views.terminar_proceso, name='terminar_proceso'),
]
