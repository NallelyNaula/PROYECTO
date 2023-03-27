from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
import io

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

from .models import proyecto, tarea, etiqueta, comentario
from .forms import ProyectoForm, TareaForm, EtiquetaForm, ComentarioForm
from .forms import BuscarProyectoForm, BuscarTareaForm, BuscarEtiquetaForm, BuscarComentarioForm


# Create your views here.

# Proyecto
def crear_proyecto(request):
    if request.method == "POST":
        proyectoForm = ProyectoForm(request.POST)
        if proyectoForm.is_valid():
            nombre = proyectoForm.cleaned_data['nombre']
            descripcion = proyectoForm.cleaned_data['descripcion']
            usuario_creacion = request.user
            usuario_modificacion = request.user
            proyecto.objects.create(nombre=nombre, descripcion=descripcion,  usuario_creacion=usuario_creacion,
                                    usuario_modificacion=usuario_modificacion)
            messages.add_message(request, messages.SUCCESS, 'Su registro fue un existo')
            return redirect('consultar_proyecto')
        else:
            messages.add_message(request, messages.WARNING, "No se registro exitosamente")
            proyectoForm = ProyectoForm()
    else:
        proyectoForm = ProyectoForm()
    return render(request, "proyecto/crear_proyecto.html", {'proyectoForm': proyectoForm})


def modificar_proyecto(request, id):
    if request.method == "POST":
        Proyecto = get_object_or_404(proyecto, pk=id)
        proyectoForm = ProyectoForm(request.POST or None, instance=Proyecto)
        if proyectoForm.is_valid():
            proyecto.usuario_modificacion = request.user
            Proyecto.save()
            ##personaForm.
            return redirect('consultar_proyecto')
    else:  ##GET
        Proyecto = get_object_or_404(proyecto, pk=id)
        proyectoForm = ProyectoForm(instance=Proyecto)
    return render(request, "proyecto/modificar_proyecto.html", {'proyectoForm': proyectoForm})


def consultar_proyecto(request):
    buscarproyecto = BuscarProyectoForm()
    proyectos = proyecto.objects.filter(estado=1)
    return render(request, "proyecto/consultar_proyecto.html",
                  {"lista_proyectos": proyectos, 'buscar_proyecto': buscarproyecto})


def buscar_proyecto(request):
    if request.method == "POST":
        buscarproyecto = BuscarProyectoForm(request.POST or None)
        if buscarproyecto.is_valid():
            nombre = buscarproyecto.cleaned_data['nombre']
            desde = buscarproyecto.cleaned_data['desde']
            hasta = buscarproyecto.cleaned_data['hasta']
            proyectos = proyecto.objects.filter(
                Q(nombre__contains=nombre) and Q(fecha_creacion__range=(desde, hasta)))
        else:
            proyectos = proyecto.objects.filter(estado=1)
            buscarproyecto = BuscarProyectoForm()
    return render(request, "proyecto/consultar_proyecto.html",
                  {'buscar_proyecto': buscarproyecto, "lista_proyectos": proyectos})


def eliminar_proyecto(request, id):
    if request.method == "POST":
        Proyecto = get_object_or_404(proyecto, pk=id)
        proyectoForm = ProyectoForm(request.POST or None, instance=Proyecto)
        if proyectoForm.is_valid():
            proyecto.usuario_modificacion = request.user
            proyecto.estado = 0
            Proyecto.save()
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            ##personaForm.
            return redirect('consultar_proyecto')
    else:  ##GET
        Proyecto = get_object_or_404(proyecto, pk=id)
        proyectoForm = ProyectoForm(instance=Proyecto)
    return render(request, "proyecto/eliminar_proyecto.html", {'proyectoForm': proyectoForm})


def exportar_lista_proyecto(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_proyecto.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        proyectos = []
        styles = getSampleStyleSheet()
        header = Paragraph("  Reporte De proyecto", styles['Heading1'])
        proyectos.append(header)

        buscarproyecto = BuscarProyectoForm(request.POST or None)
        if buscarproyecto.is_valid():
            # nombre = buscarproyecto.cleaned_data['nombre']
            # desde = buscarproyecto.cleaned_data['desde']
            # hasta = buscarproyecto.cleaned_data['hasta']
            # lista_proyecto = proyecto.objects.filter(
            #     Q(fecha_creacion_range=(desde, hasta)) & Q(categoriadescripcion_startswith=categoria))

            lista_proyectos = proyecto.objects.all()
            headings = ('Nombre', 'Descripcion', 'Estado')
            allproyectos = [(p.nombre, p.descripcion, p.estado)
                            for p in lista_proyectos]

            t = Table([headings] + allproyectos)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            proyectos.append(t)
            doc.build(proyectos)
            response.write(buffer.getvalue())
            buffer.close()

    return response


# Tarea

def crear_tarea(request):
    if request.method == "POST":
        tareaForm = TareaForm(request.POST or None)
        if tareaForm.is_valid():
            tareaForm.save()
            messages.add_message(request, messages.SUCCESS, 'su resgistro fue un existo')
            return redirect('consultar_tarea')
    else:
        tareaForm = TareaForm()
    return render(request, "tarea/crear_tarea.html", {'form': tareaForm})


def modificar_tarea(request, id):
    if request.method == "POST":
        Tarea = get_object_or_404(tarea, pk=id)
        tareaForm = TareaForm(request.POST or None, instance=Tarea)
        if tareaForm.is_valid():
            tareaForm.save()
            return redirect('consultar_tarea')
    else:  # GET
        Tarea = get_object_or_404(tarea, pk=id)
        tareaForm = TareaForm(instance=Tarea)
    return render(request, "tarea/modificar_tarea.html", {'form': tareaForm})


def consultar_tarea(request):
    buscartarea = BuscarTareaForm()
    tareas = tarea.objects.filter(estado=1)
    return render(request, "tarea/consultar_tarea.html",
                  {"lista_tareas": tareas, 'buscar_tarea': buscartarea})


def buscar_tarea(request):
    if request.method == "POST":
        buscartarea = BuscarTareaForm(request.POST or None)
        if buscartarea.is_valid():
            nombre = buscartarea.cleaned_data['nombre']
            desde = buscartarea.cleaned_data['desde']
            hasta = buscartarea.cleaned_data['hasta']
            tareas = tarea.objects.filter(
                Q(nombre__contains=nombre) and Q(fecha_creacion__range=(desde, hasta)))
        else:
            tareas = tarea.objects.filter(estado=1)
            buscartarea = BuscarTareaForm()
    return render(request, "tarea/consultar_tarea.html",
                  {'buscar_tarea': buscartarea, "lista_tareas": tareas})


def eliminar_tarea(request, id):
    if request.method == "POST":
        Tarea = get_object_or_404(tarea, pk=id)
        tareaForm = TareaForm(request.POST or None, instance=Tarea)
        if tareaForm.is_valid():
            tareaForm.save(commit=False)
            Tarea.estado = 0
            tareaForm.save(commit=True)
            return redirect('consultar_tarea')
    else:  # GET
        Tarea = get_object_or_404(tarea, pk=id)
        tareaForm = TareaForm(instance=Tarea)
    return render(request, "tarea/eliminar_tarea.html", {'form': tareaForm})


def exportar_lista_tarea(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_tarea.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        tareas = []
        styles = getSampleStyleSheet()
        header = Paragraph("  Reporte De Tarea", styles['Heading1'])
        tareas.append(header)

        buscartarea = BuscarTareaForm(request.POST or None)
        if buscartarea.is_valid():
            # nombre = buscartarea.cleaned_data['nombre']
            # desde = buscartarea.cleaned_data['desde']
            # hasta = buscartarea.cleaned_data['hasta']
            # lista_tarea = tarea.objects.filter(
            #     Q(fecha_creacion_range=(desde, hasta)) & Q(categoriadescripcion_startswith=categoria))

            lista_tareas = tarea.objects.all()
            headings = ('Nombre', 'Descripcion', 'Fecha_Inicio', 'Fecha_Fin', 'Proyecto', 'Estado')
            alltareas = [(t.nombre, t.descripcion, t.fecha_inicio, t.fecha_fin, t.proyecto, t.estado)
                        for t in lista_tareas]

            t = Table([headings] + alltareas)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            tareas.append(t)
            doc.build(tareas)
            response.write(buffer.getvalue())
            buffer.close()

    return response


# Etiqueta

def crear_etiqueta(request):
    if request.method == "POST":
        etiquetaForm = TareaForm(request.POST or None)
        if etiquetaForm.is_valid():
            etiquetaForm.save()
            messages.add_message(request, messages.SUCCESS, 'su resgistro fue un existo')
            return redirect('consultar_etiqueta')
    else:
        etiquetaForm = EtiquetaForm()
    return render(request, "etiqueta/crear_etiqueta.html", {'form': etiquetaForm})


def modificar_etiqueta(request, id):
    if request.method == "POST":
        Etiqueta = get_object_or_404(etiqueta, pk=id)
        etiquetaForm = EtiquetaForm(request.POST or None, instance=Etiqueta)
        if etiquetaForm.is_valid():
            etiquetaForm.save()
            return redirect('consultar_etiqueta')
    else:  # GET
        Etiqueta = get_object_or_404(etiqueta, pk=id)
        etiquetaForm = EtiquetaForm(instance=Etiqueta)
    return render(request, "etiqueta/modificar_etiqueta.html", {'form': etiquetaForm})


def consultar_etiqueta(request):
    buscaretiqueta = BuscarEtiquetaForm()
    etiquetas = etiqueta.objects.filter(estado=1)
    return render(request, "etiqueta/consultar_etiqueta.html",
                  {"lista_etiquetas": etiquetas, 'buscar_etiqueta': buscaretiqueta})


def buscar_etiqueta(request):
    if request.method == "POST":
        buscaretiqueta = BuscarEtiquetaForm(request.POST or None)
        if buscaretiqueta.is_valid():
            nombre_etiqueta = buscaretiqueta.cleaned_data['nombre_etiqueta']
            desde = buscaretiqueta.cleaned_data['desde']
            hasta = buscaretiqueta.cleaned_data['hasta']
            etiquetas = etiqueta.objects.filter(
                Q(nombre_etiqueta__contains=nombre_etiqueta) and Q(fecha_creacion__range=(desde, hasta)))
        else:
            etiquetas = etiqueta.objects.filter(estado=1)
            buscaretiqueta = BuscarEtiquetaForm()
    return render(request, "etiqueta/consultar_etiqueta.html",
                  {'buscar_etiqueta': buscaretiqueta, "lista_etiquetas": etiquetas})


def eliminar_etiqueta(request, id):
    if request.method == "POST":
        Etiqueta = get_object_or_404(etiqueta, pk=id)
        etiquetaForm = TareaForm(request.POST or None, instance=Etiqueta)
        if etiquetaForm.is_valid():
            etiquetaForm.save(commit=False)
            etiqueta.estado = 0
            etiquetaForm.save(commit=True)
            return redirect('consultar_etiqueta')
    else:  # GET
        Etiqueta = get_object_or_404(etiqueta, pk=id)
        etiquetaForm = EtiquetaForm(instance=Etiqueta)
    return render(request, "etiqueta/eliminar_etiqueta.html", {'form': etiquetaForm})


def exportar_lista_etiqueta(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_etiqueta.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        etiquetas = []
        styles = getSampleStyleSheet()
        header = Paragraph("  Reporte De etiqueta", styles['Heading1'])
        etiquetas.append(header)

        buscaretiqueta = BuscarEtiquetaForm(request.POST or None)
        if buscaretiqueta.is_valid():
            # nombre = buscaretiqueta.cleaned_data['nombre']
            # desde = buscaretiqueta.cleaned_data['desde']
            # hasta = buscaretiqueta.cleaned_data['hasta']
            # lista_etiqueta = etiqueta.objects.filter(
            #     Q(fecha_creacion_range=(desde, hasta)) & Q(categoriadescripcion_startswith=categoria))

            lista_etiquetas = etiqueta.objects.all()
            headings = ('Nombre_Etiqueta', 'Descripcion_Etiqueta', 'Tarea', 'Estado')
            alletiquetas = [(e.nombre_etiqueta, e.descripcion_etiqueta, e.tarea, e.estado)
                           for e in lista_etiquetas]

            t = Table([headings] + alletiquetas)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            etiquetas.append(t)
            doc.build(etiquetas)
            response.write(buffer.getvalue())
            buffer.close()

    return response


# Comentario
def crear_comentario(request):
    if request.method == "POST":
        comentarioForm = ComentarioForm(request.POST or None)
        if comentarioForm.is_valid():
            comentarioForm.save()
            messages.add_message(request, messages.SUCCESS, 'su resgistro fue un existo')
            return redirect('consultar_tarea')
    else:
        comentarioForm = TareaForm()
    return render(request, "comentario/crear_comentario.html", {'form': comentarioForm})


def modificar_comentario(request, id):
    if request.method == "POST":
        Comentario = get_object_or_404(comentario, pk=id)
        comentarioForm = ComentarioForm(request.POST or None, instance=Comentario)
        if comentarioForm.is_valid():
            comentarioForm.save()
            return redirect('consultar_comentario')
    else:  # GET
        Comentario = get_object_or_404(comentario, pk=id)
        comentarioForm = ComentarioForm(instance=Comentario)
    return render(request, "comentario/modificar_comentario.html", {'form': comentarioForm})


def consultar_comentario(request):
    buscarcomentario = BuscarComentarioForm()
    comentarios = comentario.objects.filter(estado=1)
    return render(request, "comentario/consultar_comentario.html",
                  {"lista_comentarios": comentarios, 'buscar_comentario': buscarcomentario})


def buscar_comentario(request):
    if request.method == "POST":
        buscarcomentario = BuscarComentarioForm(request.POST or None)
        if buscarcomentario.is_valid():
            contenido = buscarcomentario.cleaned_data['contenido']
            desde = buscarcomentario.cleaned_data['desde']
            hasta = buscarcomentario.cleaned_data['hasta']
            comentarios = comentario.objects.filter(
                Q(contenido__contains=contenido) and Q(fecha_creacion__range=(desde, hasta)))
        else:
            comentarios = comentario.objects.filter(estado=1)
            buscarcomentario = BuscarComentarioForm()
    return render(request, "comentario/consultar_comentario.html",
                  {'buscar_comentario': buscarcomentario, "lista_comentarios": comentarios})


def eliminar_comentario(request, id):
    if request.method == "POST":
        Comentario = get_object_or_404(comentario, pk=id)
        comentarioForm = ComentarioForm(request.POST or None, instance=Comentario)
        if comentarioForm.is_valid():
            comentarioForm.save(commit=False)
            Comentario.estado = 0
            comentarioForm.save(commit=True)
            return redirect('consultar_comentario')
    else:  # GET
        Comentario= get_object_or_404(comentario, pk=id)
        comentarioForm = ComentarioForm(instance=Comentario)
    return render(request, "comentario/eliminar_comentario.html", {'form': comentarioForm})


def exportar_lista_comentario(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_comentario.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        comentarios = []
        styles = getSampleStyleSheet()
        header = Paragraph("  Reporte De comentario", styles['Heading1'])
        comentarios.append(header)

        buscarcomentario = BuscarComentarioForm(request.POST or None)
        if buscarcomentario.is_valid():
            # nombre = buscarcomentario.cleaned_data['nombre']
            # desde = buscarcomentario.cleaned_data['desde']
            # hasta = buscarcomentario.cleaned_data['hasta']
            # lista_comentario = comentario.objects.filter(
            #     Q(fecha_creacion_range=(desde, hasta)) & Q(categoriadescripcion_startswith=categoria))

            lista_comentarios = comentario.objects.all()
            headings = ('Contenido', 'Fecha_Comentario', 'Tarea', 'Estado')
            allcomentarios = [(c.contenido, c.fecha_comentario, c.tarea, c.estado)
                              for c in lista_comentarios]

            t = Table([headings] + allcomentarios)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            comentarios.append(t)
            doc.build(comentarios)
            response.write(buffer.getvalue())
            buffer.close()

        return response
