from django.urls import path
from . import views

urlpatterns = [
    path('', views.monitor_procesos_windows, name='monitor_procesos_windows'),
    path('terminar_proceso_windows/', views.terminar_proceso_windows, name='terminar_proceso_windows'),
]
