from django.forms import Form
from django import forms
from .models import proyecto, tarea, etiqueta, comentario


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = proyecto
        fields = ['nombre', 'descripcion']


class BuscarProyectoForm(Form):
    nombre = forms.CharField(max_length=255)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={
        'placeholder': 'Seleccione una fecha',
        'type': 'date', 'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={
        'placeholder': 'Seleccione una fecha', 'type': 'date', 'size': 30}))


class TareaForm(forms.ModelForm):
    class Meta:
        model = tarea
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'proyecto']
        widgets = {'fecha_inicio': forms.DateInput(format=('%Y-%m-%d'),
                                                   attrs={
                                                       'placeholder': 'Select a date',
                                                       'type': 'date',
                                                       'size': 30}),
                   'fecha_fin': forms.DateInput(format=('%Y-%m-%d'),
                                                attrs={
                                                    'placeholder': 'Select a date',
                                                    'type': 'date',
                                                    'size': 30})}


class BuscarTareaForm(Form):
    nombre = forms.CharField(max_length=255)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={
        'placeholder': 'Seleccione una fecha',
        'type': 'date', 'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={
        'placeholder': 'Seleccione una fecha', 'type': 'date', 'size': 30}))


class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = etiqueta
        fields = ['nombre_etiqueta', 'descripcion_etiqueta', 'tarea']


class BuscarEtiquetaForm(Form):
    nombre_etiqueta = forms.CharField(max_length=255)
    desde = forms.DateTimeField(label="Desde", required=True,
                                widget=forms.DateInput(format=('%Y-%m-%d'), attrs={
                                    'placeholder': 'Seleccione una fecha',
                                    'type': 'date', 'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True,
                                widget=forms.DateInput(format=('%Y-%m-%d'), attrs={
                                    'placeholder': 'Seleccione una fecha', 'type': 'date', 'size': 30}))


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = comentario
        fields = ['contenido', 'fecha_comentario', 'tarea']
        widgets = {'fecha_comentario': forms.DateInput(format=('%Y-%m-%d'),
                                                       attrs={
                                                           'placeholder': 'Select a date',
                                                           'type': 'date',
                                                           'size': 30})}


class BuscarComentarioForm(Form):
    contenido = forms.CharField(max_length=255)
    desde = forms.DateTimeField(label="Desde", required=True,
                                widget=forms.DateInput(format=('%Y-%m-%d'), attrs={
                                    'placeholder': 'Seleccione una fecha',
                                    'type': 'date', 'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True,
                                widget=forms.DateInput(format=('%Y-%m-%d'), attrs={
                                    'placeholder': 'Seleccione una fecha', 'type': 'date', 'size': 30}))
