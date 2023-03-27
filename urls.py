from django.urls import path
from . import views

urlpatterns = [

    path('crear_proyecto', views.crear_proyecto, name="crear_proyecto"),
    path('modificar_proyecto <int:id> ', views.modificar_proyecto, name="modificar_proyecto"),
    path('consultar_proyecto', views.consultar_proyecto, name="consultar_proyecto"),
    path('eliminar_proyecto <int:id>', views.eliminar_proyecto, name="eliminar_proyecto"),
    path('buscar_proyecto', views.buscar_proyecto, name="buscar_proyecto"),
    path('exportar_lista_proyecto', views.exportar_lista_proyecto, name="exportar_lista_proyecto"),

    path('crear_tarea', views.crear_tarea, name="crear_tarea"),
    path('modificar_tarea <int:id> ', views.modificar_tarea, name="modificar_tarea"),
    path('consultar_tarea', views.consultar_tarea, name="consultar_tarea"),
    path('eliminar_tarea <int:id>', views.eliminar_tarea, name="eliminar_tarea"),
    path('buscar_tarea', views.buscar_tarea, name="buscar_tarea"),
    path('exportar_lista_tarea', views.exportar_lista_tarea, name="exportar_lista_tarea"),

    path('crear_etiqueta', views.crear_etiqueta, name="crear_etiqueta"),
    path('modificar_etiqueta <int:id> ', views.modificar_etiqueta, name="modificar_etiqueta"),
    path('consultar_etiqueta', views.consultar_etiqueta, name="consultar_etiqueta"),
    path('eliminar_etiqueta <int:id>', views.eliminar_etiqueta, name="eliminar_etiqueta"),
    path('buscar_etiqueta', views.buscar_etiqueta, name="buscar_etiqueta"),
    path('exportar_lista_etiqueta', views.exportar_lista_etiqueta, name="exportar_lista_etiqueta"),

    path('crear_comentario', views.crear_comentario, name="crear_comentario"),
    path('modificar_comentario <int:id> ', views.modificar_comentario, name="modificar_comentario"),
    path('consultar_comentario', views.consultar_comentario, name="consultar_comentario"),
    path('eliminar_comentario <int:id>', views.eliminar_comentario, name="eliminar_comentario"),
    path('buscar_comentario', views.buscar_comentario, name="buscar_comentario"),
    path('exportar_lista_comentario', views.exportar_lista_comentario, name="exportar_lista_comentario"),

]
