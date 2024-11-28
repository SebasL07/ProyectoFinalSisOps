from django.urls import path
from . import views

urlpatterns = [
    path('', views.monitor_procesos_linux, name='monitor_procesos_linux'),
    path('terminar_proceso_linux/', views.terminar_proceso_linux, name='terminar_proceso_linux'),
]
