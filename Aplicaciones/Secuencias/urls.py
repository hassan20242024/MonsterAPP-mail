from django.urls import path

from . import views

urlpatterns=[
   
    path("crear_secuencias/",views.crear_secuencias, name="crear_secuencias"),
    #path("editar_secuencias/<int:pk>/", views.editar_secuencias, name="editar_secuencias"),
    path("actualizar_secuencias_validadas/<int:pk>/", views.actualizar_secuencias_validadas,name="actualizar_secuencias_validadas"),
    path("cambiar_estado_ensayo/<int:pk>/", views.cambiar_estado_ensayo,name="cambiar_estado_ensayo"),
    #path("actualizar_secuencias_impresas/<int:pk>/", views.actualizar_secuencias_impresas, name="actualizar_secuencias_impresas"),
    #path("actualizar_secuencias_reportadas/<int:pk>/", views.actualizar_secuencias_reportadas, name="actualizar_secuencias_reportadas"),
    path("crear_secuencias_en_curso/",views.crear_secuencias_en_curso, name="crear_secuencias_en_curso"),
    path("editar_secuencias_en_curso/<int:pk>/", views.editar_secuencias_en_curso, name="editar_secuencias_en_curso"),
    path("agregar_otra_secuencia_parametro/<int:pk>/", views.agregar_otra_secuencia_parametro, name="agregar_otra_secuencia_parametro"),
    path("agregar_otra_secuencia_muestra/<int:pk>/", views.agregar_otra_secuencia_muestra, name="agregar_otra_secuencia_muestra"),
    path("proceso_secuencias_en_curso/",views.proceso_secuencias_en_curso, name="proceso_secuencias_en_curso"),
    path("secuencias_invalidas/",views.secuencias_invalidas, name="secuencias_invalidas"),
    path("chart_js_proceso_secuencias_en_curso/",views.chart_js_proceso_secuencias_en_curso, name="chart_js_proceso_secuencias_en_curso"),
    path("mantenimientos_periodicos/",views.mantenimientos_periodicos, name="mantenimientos_periodicos"),
    path("mantenimientos_buzos_realizados/",views.mantenimientos_buzos_realizados, name="mantenimientos_buzos_realizados"),
    path("mantenimientos_celdas_realizados/",views.mantenimientos_celdas_realizados, name="mantenimientos_celdas_realizados"),
    path("mantenimientos_test_realizados/",views.mantenimientos_test_realizados, name="mantenimientos_test_realizados"),
    path("mantenimientos_preventivo_realizado/",views.mantenimientos_preventivo_realizado, name="mantenimientos_preventivo_realizado"),
    path("calificaciones_realizadas/",views.calificaciones_realizadas, name="calificaciones_realizadas"),
    path("mantenimientos_buzos_Check_form/", views.mantenimientos_buzos_Check_form, name="mantenimientos_buzos_Check_form"),
    path("cambiar_estado_secuencias/", views.cambiar_estado_secuencias, name="cambiar_estado_secuencias"),
    path("cambiar_estado_validada_revisada/", views.cambiar_estado_validada_revisada, name="cambiar_estado_validada_revisada"),



  
]