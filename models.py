from django.db import models
from django.db.models import ForeignKey
from registro.models import Usuario


class proyecto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuario_creacion")
    usuario_modificacion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuario_modificacion")

    class Meta:
        db_table = "proyecto"
        verbose_name = "proyecto"
        verbose_name_plural = "proyecto"
        ordering = ['fecha_creacion', 'nombre']

    def __str__(self):
        return '{}'.format(self.nombre)


class tarea(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    proyecto = ForeignKey(proyecto, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "tarea"
        verbose_name = "tarea"
        verbose_name_plural = "tarea"
        ordering = ['fecha_creacion', 'nombre']

    def __str__(self):
        return '{}'.format(self.nombre)


class etiqueta(models.Model):
    nombre_etiqueta = models.CharField(max_length=255)
    descripcion_etiqueta = models.CharField(max_length=255)
    tarea = ForeignKey(tarea, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "etiqueta"
        verbose_name = "etiqueta"
        verbose_name_plural = "etiquetas"
        ordering = ['fecha_creacion', 'nombre_etiqueta']

    def __str__(self):
        return '{}'.format(self.nombre_etiqueta)


class comentario(models.Model):
    contenido = models.CharField(max_length=255)
    fecha_comentario = models.DateTimeField()
    tarea = ForeignKey(tarea, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)
    class Meta:
        db_table = "comentario"
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"
        ordering = ['fecha_creacion', 'contenido']

    def __str__(self):
        return '{}'.format(self.contenido)
