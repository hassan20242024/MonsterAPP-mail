from django.urls import path

from . import views

urlpatterns=[
    #path("protocolo_metodos/",views.protocolo_metodos, name="protocolo_metodos"),
    path("protocolo_proceso/",views.protocolo_proceso, name="protocolo_proceso"),
    path("editar_protocolo_proceso/<int:pk>/", views.editar_protocolo_proceso, name="editar_protocolo_proceso"),
    path("crear_protocolo_proceso/", views.crear_protocolo_proceso, name="crear_protocolo_proceso"),
    path("revisar_protocolo_proceso/<int:pk>/", views.revisar_protocolo_proceso, name="revisar_protocolo_proceso"),

]