from django.shortcuts import render, redirect
from .models import Secuencias,Proceso,Muestras_y_Placebos, Protocolos, Parametro,Metodo, Ensayo, Sistema, Perfil,usuario_invalidar,usuario_validar, usuario_reporte,usuario_impresion,usuario_auditor,Lavado_buzo
from .forms import secuenciasForm, buzosForm
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Q
import json
from django.core.exceptions import ValidationError
from datetime import datetime
import datetime
from django.utils import formats
from django.shortcuts import render
from django.http import JsonResponse 
from dateutil.relativedelta import relativedelta, MO

# Create your views here.


@login_required
def crear_secuencias(request):
    titulo="Crear Secuencias"
    secuenicas=Secuencias.objects.all()
    protocolos=Protocolos.objects.all()
    parametros=Parametro.objects.all()
    ensayo=Ensayo.objects.all()
   
    if request.method == "POST":
        form = secuenciasForm(request.POST)
       
        if form.is_valid():
            form.save()
            messages.success(request, "Creada con éxito")
           
            return redirect("crear_secuencias_en_curso")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
             return redirect("crear_secuencias_en_curso")  
    else:
        form = secuenciasForm() 
        
    context={
        "titulo":titulo,
        "form":form,
        
        
        "secuenicas":secuenicas,
        "protocolos":protocolos,
        "parametros":parametros,
         "ensayo":ensayo,
    }
    
    return render(request, "secuencias/crear_secuencias_en_curso.html", context)

@login_required
def crear_secuencias_en_curso(request):
    #titulo="Crear Secuencias"
    pkt = Protocolos.objects.values("parametro")
    secuencias1=Secuencias.objects.values("parametro_sq")
    secuenicas=Secuencias.objects.all()
    metodo=Metodo.objects.all()
    protocolos=Protocolos.objects.all()
    protocolo_proceso =Proceso.objects.all()
    parametros=Parametro.objects.all()
    ensayo=Ensayo.objects.all()
    sistema=Sistema.objects.all()
    #invalidez=Invalidar_Secuencia.objects.all
    usuario=Perfil.objects.all()
    invalidar=usuario_invalidar.objects.filter(usuario=request.user)
    validar=usuario_validar.objects.filter(usuario=request.user)
    protocolos_proceso=Proceso.objects.all()
    muestras=Muestras_y_Placebos.objects.all()

    sist=Sistema.objects.filter(id=1)
   
    if request.method == "POST":
        form = secuenciasForm(request.POST)
       
        if form.is_valid() and secuencias1 == pkt:
            form.save()
            messages.success(request, "Creada con éxito")
           
            return redirect("crear_secuencias_en_curso")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
             return redirect("crear_secuencias_en_curso")  
    else:
        form = secuenciasForm() 
        
    context={
        #"titulo":titulo,
        "metodo":metodo,
        "invalidar":invalidar,
        "validar":validar,
        "form":form,
        #"invalidez":invalidez,
        "secuenicas":secuenicas,
        "protocolos":protocolos,
        "parametros":parametros,
         "ensayo":ensayo,
         "sistema":sistema,
         "usuario":usuario,
         "protocolos_proceso":protocolos_proceso,
         "muestras":muestras,
         "protocolo_proceso":protocolo_proceso,
        
        
         #"parametro_dependiente":parametro_dependiente,
    }
    return render(request, "secuencias/crear_secuencias_en_curso.html", context)

@login_required
def proceso_secuencias_en_curso(request):
    secuenicas=Secuencias.objects.all()
    protocolos=Protocolos.objects.all()
    protocolo_proceso =Proceso.objects.all()
    muestras=Muestras_y_Placebos.objects.all()
    metodo=Metodo.objects.all()
    parametros=Parametro.objects.all()
    ensayo=Ensayo.objects.all()
    sistema=Sistema.objects.all()
    #invalidez=Invalidar_Secuencia.objects.all
    invalidar=usuario_invalidar.objects.filter(usuario=request.user)
    validar=usuario_validar.objects.filter(usuario=request.user)
    imprimir=usuario_impresion.objects.filter(usuario=request.user)
    reportar=usuario_reporte.objects.filter(usuario=request.user)
    auditar=usuario_auditor.objects.filter(usuario=request.user)
    usuarios=Perfil.objects.all()
    secuencia=Secuencias.objects.all()
    #secuenciasp = Secuencias.objects.filter(protocolo=1)
    super_usuario=Perfil.objects.all()
    #secuencias1=Reporte.objects.filter(pk=1)
        
    context={
        #"titulo":titulo,
        #"secuenciasp":secuenciasp,
        "invalidar":invalidar,
        "validar":validar,
        #"invalidez":invalidez,
        "secuenicas":secuenicas,
        "protocolos":protocolos,
        "parametros":parametros,
         "ensayo":ensayo,
         "sistema":sistema,
         "reportar":reportar,
         "secuencia":secuencia,
         "super_usuario":super_usuario,
        "auditar":auditar,
         "imprimir":imprimir,
         "usuarios":usuarios,
         "protocolo_proceso":protocolo_proceso,
         "muestras":muestras,
         "metodo":metodo,
         #"secuencias1":secuencias1,
    
    }
    return render(request, "secuencias/proceso_secuencias_en_curso.html", context)

@login_required
def secuencias_invalidas(request):
    secuencias=Secuencias.objects.all()
    validar=usuario_validar.objects.filter(usuario=request.user)
        
    context={
        #"titulo":titulo,
        "secuencias":secuencias,
        "validar":validar
    }
    return render(request, "secuencias/secuencias_invalidas.html", context)

@login_required
def chart_js_proceso_secuencias_en_curso(request):
   registro_total = Secuencias.objects.count()
   pendientes_validaciones = Secuencias.objects.filter(status="Registrada").count()
   pendientes_impresiones = Secuencias.objects.filter(status="Revisada").count()
   pendientes_reportes = Secuencias.objects.filter(status="Impresa").count()
   pendientes_auditorias = Secuencias.objects.filter(status="Reportada").count()
   invalidas = Secuencias.objects.filter(status="Invalida").count()
   ensayos = Secuencias.objects.filter(status="Ensayo").count()
   total_grafico_pie_secuencias=pendientes_validaciones+pendientes_impresiones+pendientes_reportes+pendientes_auditorias
   if total_grafico_pie_secuencias > 0:
    procentaje_pendientes_validaciones=pendientes_validaciones*100/total_grafico_pie_secuencias
    procentaje_pendientes_impresiones=pendientes_impresiones*100/total_grafico_pie_secuencias
    procentaje_pendientes_reportes=pendientes_reportes*100/total_grafico_pie_secuencias
    procentaje_pendientes_auditorias=pendientes_auditorias*100/total_grafico_pie_secuencias
   else:
       procentaje_pendientes_validaciones=pendientes_validaciones*100/1
       procentaje_pendientes_impresiones=pendientes_impresiones*100/1
       procentaje_pendientes_reportes=pendientes_reportes*100/1
       procentaje_pendientes_auditorias=pendientes_auditorias*100/1
        

   pendiente_validación = Secuencias.objects.filter(status="Registrada").count()
   pendiente_impresion = Secuencias.objects.filter(status="Revisada").count()
   pendiente_reporte = Secuencias.objects.filter(status="Impresa").count()
   pendientes_auditoria = Secuencias.objects.filter(status="Reportada").count()
   chart1 = {
        'chart': {'type': 'pie'},
        'title': {'text': ''},
         "credits": "false",
               "plotOptions": {
		"pie": {
			"pointPadding": 0,
			"borderWidth": 8,
		}
	},
        'series': [{
             "name": "Status",
            'data': [{
            'y': pendiente_validación,
            'name':  '%s°/° Adquiriendo'% int(procentaje_pendientes_validaciones),
            'color': "#FF6384",
        }, {
            'y': pendiente_impresion,
            'name':  '%s°/° Impresiones pendientes'  %int(procentaje_pendientes_impresiones),
            'color':  "#63FF84", 
        },{
         'y': pendiente_reporte,
            'name':  '%s°/° Reportes pendientes'  %int(procentaje_pendientes_reportes),
            'color': "#8463FF",
        }, {
         'y': pendientes_auditoria,
            'name':  '%s°/° Pendientes por auditar'  %int(procentaje_pendientes_auditorias),
            'color': "#6384FF" 
        }
        ]
        }]
    }
   chart1A = {
        'chart': {'type': 'column'},
        'title': {'text': ''},
         "credits": "false",
          "xAxis": {
            "categories": ['Adquiriendo', 'Impresiones pendientes', 'Reportes pendientes', 'Pendientes por auditar']
        },
         "plotOptions": {
		"column": {
			"pointPadding": 0.2,
			"borderWidth": 15,
               #"borderColor": "#417690",
		}
	},
        'series': [{
            "name": "Status",
            'data': [{
            'y': pendiente_validación,
            'name': "Adquiriendo",
            'color': "#FF6384",
            
        }, {
            'y': pendiente_impresion,
            'name': "Impresiones pendientes",
            'color':  "#63FF84",
        },{
         'y': pendiente_reporte,
            'name': "Reportes pendientes",
            'color':"#8463FF",    
        }, {
         'y': pendientes_auditoria,
            'name': "Pendientes por auditar",
            'color': "#6384FF"    
        }
        ]
        }]
    }
   dataset = Secuencias.objects \
        .values('sistema__nombre') \
        .annotate(registrada=Count('sistema', filter=Q(status="Registrada")),
                  validada=Count('sistema', filter=Q(status="Revisada")),
                  impresa=Count('sistema', filter=Q(status="Impresa"))) \
        .order_by('-sistema')

   categories = []
   registrada = list()
   validada = list()
   impresa = list()
   for entry in dataset:
        categories.append('%s ' % entry['sistema__nombre'])
        registrada.append(entry['registrada'])
        validada.append(entry['validada'])
        impresa.append(entry['impresa'])
   registrada_series = {
        'name': ' Adquiriendo',
        'data': registrada,
        'color': "#FF6384",
    }

   validada_series = {
        'name': 'Impresiones pendientes',
        'data': validada,
        'color': "#63FF84",
    }
   impresa_series = {
        'name': 'Reportes pendientes',
        'data': impresa,
        'color': "#8463FF",
    }
   chart = {
        'chart': {'type': 'column' },
        "credits": "false",

        'title': {'text': ''},
        'xAxis': {'categories': categories},
        'series': [registrada_series, validada_series, impresa_series],
    }
   dump = json.dumps(chart)
   return render(request, 'secuencias/chart_js__proceso_secuencias_en_curso.html', {'chart': dump, "chart1":chart1,"chart1A":chart1A,
    "registro_total":registro_total, "pendientes_validaciones":pendientes_validaciones,"pendientes_impresiones":pendientes_impresiones,
    "pendientes_reportes":pendientes_reportes, "invalidas":invalidas, "pendientes_auditorias":pendientes_auditorias, "ensayos":ensayos})

@login_required
def editar_secuencias_en_curso(request, pk):
    titulo="Crear Secuencias"
  
    secuencia=Secuencias.objects.get(id=pk)
    protocolos=Protocolos.objects.all()
    parametros=Parametro.objects.all()
    sistema=Sistema.objects.all()
    sq=Secuencias.objects.filter(id=pk)
    protocolo_proceso =Proceso.objects.all()

    ensayo=Ensayo.objects.all()

   
    if request.method == "POST":
        form = secuenciasForm(request.POST, instance=secuencia)
       
        if form.is_valid():
            form.save()
            messages.success(request, "La secuencia ha sido actualizada")
           
            return redirect("crear_secuencias_en_curso")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
             return redirect("crear_secuencias_en_curso")    
    else:
        form = secuenciasForm(instance=secuencia) 
        
    context={
        "titulo":titulo,
        "form":form,
        "protocolos":protocolos,
        "parametros":parametros,
         "ensayo":ensayo,
         "sistema":sistema,
         "secuencia":secuencia,
         "sq":sq,
         "protocolo_proceso":protocolo_proceso
    }
    return render(request, "secuencias/editar_secuencias_en_curso.html", context)

@login_required
def agregar_otra_secuencia_parametro(request, pk):
    titulo="Crear Secuencias"
  
    secuencia=Secuencias.objects.get(id=pk)
    protocolos=Protocolos.objects.all()
    parametros=Parametro.objects.all()
    sistema=Sistema.objects.all()

    ensayo=Ensayo.objects.all()

   
    if request.method == "POST":
        form = secuenciasForm(request.POST)
       
        if form.is_valid():
            form.save()
            messages.success(request, "La secuencia ha sido agregada")
           
            return redirect("crear_secuencias_en_curso")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
             return redirect("crear_secuencias_en_curso")    
    else:
        form = secuenciasForm(instance=secuencia) 
        
    context={
        "titulo":titulo,
        "form":form,
        
        
        
        "protocolos":protocolos,
        "parametros":parametros,
         "ensayo":ensayo,
         "sistema":sistema,
         "secuencia":secuencia,
    }
    return render(request, "secuencias/agregar_otra_secuencia_parametro.html", context)

@login_required
def agregar_otra_secuencia_muestra(request, pk):
    titulo="Crear Secuencias"
    secuencia=Secuencias.objects.get(id=pk)
    protocolos=Protocolos.objects.all()
    parametros=Parametro.objects.all()
    sistema=Sistema.objects.all()
    ensayo=Ensayo.objects.all()
    muestras=Muestras_y_Placebos.objects.all()
    if request.method == "POST":
        form = secuenciasForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La secuencia ha sido agregada")
            return redirect("crear_secuencias_en_curso")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
             return redirect("crear_secuencias_en_curso")    
    else:
        form = secuenciasForm(instance=secuencia) 
    context={
        "titulo":titulo,
        "form":form,
        "protocolos":protocolos,
        "parametros":parametros,
         "ensayo":ensayo,
         "sistema":sistema,
         "secuencia":secuencia,
         "muestras":muestras,
    }
    return render(request, "secuencias/agregar_otra_secuencia_muestra.html", context)

@login_required
def actualizar_secuencias_validadas(request, pk):
   titulo="Crear Secuencias"
  
   secuencia=Secuencias.objects.get(id=pk)
   protocolos=Protocolos.objects.all()
   parametros=Parametro.objects.all()
   sistema=Sistema.objects.all()
   ensayo=Ensayo.objects.all()

   if request.method == "POST":
        form = secuenciasForm(request.POST, instance=secuencia)
       
        if form.is_valid():
            form.save()
            messages.success(request, "La secuencia ha sido actualizada")
           
            return redirect("proceso_secuencias_en_curso")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
             return redirect("crear_secuencias_en_curso")    
   else:
        form = secuenciasForm(instance=secuencia) 
        
   context={
        "titulo":titulo,
        "form":form,
        
        "protocolos":protocolos,
        "parametros":parametros,
         "ensayo":ensayo,
         "sistema":sistema,
         "secuencia":secuencia,
    }
   return render(request, "secuencias/actualizar_secuencias_validadas.html", context)

@login_required
def cambiar_estado_ensayo(request, pk):
   titulo="Crear Secuencias"
  
   secuencia=Secuencias.objects.get(id=pk)
   protocolos=Protocolos.objects.all()
   parametros=Parametro.objects.all()
   sistema=Sistema.objects.all()
   ensayo=Ensayo.objects.all()

   if request.method == "POST":
        form = secuenciasForm(request.POST, instance=secuencia)
       
        if form.is_valid():
            form.save()
            Secuencias.objects.filter(id=pk).update(
        status="Ensayo", )
            messages.success(request, "La secuencia ha sido actualizada")
           
            return redirect("proceso_secuencias_en_curso")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
             return redirect("crear_secuencias_en_curso")    
   else:
        form = secuenciasForm(instance=secuencia) 
        
   context={
        "titulo":titulo,
        "form":form,
        
        "protocolos":protocolos,
        "parametros":parametros,
         "ensayo":ensayo,
         "sistema":sistema,
         "secuencia":secuencia,
    }
   return render(request, "secuencias/cambiar_estado_ensayo.html", context)

def mantenimientos_periodicos(request):
    titulo="Mantenimientos Periódicos"
    lavado_buzo=Lavado_buzo.objects.all()
    sistema=Sistema.objects.all()
    date_joined = datetime.datetime.now()
    formatedDate = date_joined.strftime("%Y-%m-%d %H:%M:%S")
    progrmado = date_joined + datetime.timedelta(days=30)
    programados=Lavado_buzo.objects.filter(fecha_lavado_buzo=progrmado)
    realizado_por=usuario_validar.objects.filter(usuario=request.user)
    context={
        "titulo":titulo,
        "lavado_buzo":lavado_buzo,
        "sistema":sistema,
        "realizado_por":realizado_por,
        "programados":programados,
        formatedDate:formatedDate
    }
    return render(request, "secuencias/mantenimientos_periodicos.html", context)

@login_required
def mantenimientos_buzos_realizados(request):
    titulo="Mantenimientos Periódicos"
    lavado_buzo=Lavado_buzo.objects.all()
    context={
        "titulo":titulo,
        "lavado_buzo":lavado_buzo,
    }
    return render(request, "secuencias/mantenimientos_buzos_realizados.html", context)

@login_required
def mantenimientos_celdas_realizados(request):
    titulo="Mantenimientos Periódicos"
    lavado_buzo=Lavado_buzo.objects.all()
    context={
        "titulo":titulo,
        "lavado_buzo":lavado_buzo,
    }
    return render(request, "secuencias/mantenimientos_celdas_realizados.html", context)

@login_required
def mantenimientos_test_realizados(request):
    titulo="Mantenimientos Periódicos"
    lavado_buzo=Lavado_buzo.objects.all()
    context={
        "titulo":titulo,
        "lavado_buzo":lavado_buzo,
    }
    return render(request, "secuencias/mantenimientos_test_realizados.html", context)

@login_required
def mantenimientos_preventivo_realizado(request):
    titulo="Mantenimientos Periódicos"
    lavado_buzo=Lavado_buzo.objects.all()
    context={
        "titulo":titulo,
        "lavado_buzo":lavado_buzo,
    }
    return render(request, "secuencias/mantenimientos_preventivo_realizado.html", context)

@login_required
def calificaciones_realizadas(request):
    titulo="Mantenimientos Periódicos"
    lavado_buzo=Lavado_buzo.objects.all()
    context={
        "titulo":titulo,
        "lavado_buzo":lavado_buzo,
    }
    return render(request, "secuencias/calificaciones_realizadas.html", context)


def mantenimientos_buzos_Check_form(request):
   #date_joineds = datetime.datetime.now()
    #progrmado = date_joined + datetime.timedelta(days=30)
   if request.method=="POST":
     mantenimientos_id=request.POST.getlist("item") #check lavado buzos
     mantenimientos_celdas_id=request.POST.getlist("itemCelda") #check lavado de celda
     mantenimientos_test_id=request.POST.getlist("itemTest") #check test de diagnostico
     mantenimientos_preventivo=request.POST.getlist("itemMantenimiento") #check antenimiento
     calificacion_realizada=request.POST.getlist("itemCalificacion") #check calificacion
     for id in mantenimientos_id: #accion seleccionada lavado de buzos
         mantenimientos_buzos=Lavado_buzo.objects.get(pk=id)
         mantenimientos_buzos.status= Lavado_buzo.Status.PROGRAMADO
         #mantenimientos_buzos.fecha_lavado_buzo= Lavado_buzo.progrmado
         mantenimientos_buzos.fecha_lavado_buzo= datetime.datetime.now() + datetime.timedelta(days=30)
         #mantenimientos_buzos.fecha_alerta_inferior= Lavado_buzo.limite_inferior
         mantenimientos_buzos.fecha_alerta_inferior= datetime.datetime.now() + datetime.timedelta(days=27)
         #mantenimientos_buzos.fecha_alerta_superior= Lavado_buzo.limite_superior
         mantenimientos_buzos.fecha_alerta_superior= datetime.datetime.now() + datetime.timedelta(days=33)
         mantenimientos_buzos.save()
         mantenimientos_buzos.pk = None #Crea una copia 
         mantenimientos_buzos.status= Lavado_buzo.Status.REALIZADO
         mantenimientos_buzos.status_celda= Lavado_buzo.Status_celda.PENDIENTE
         mantenimientos_buzos.status_test= Lavado_buzo.Status_test.PENDIENTE
         mantenimientos_buzos.status_mantenimiento= Lavado_buzo.Status_mantenimiento.PENDIENTE
         mantenimientos_buzos.status_calificacion= Lavado_buzo.Status_calificacion.PENDIENTE
         mantenimientos_buzos.fecha_lavado_buzo= datetime.datetime.now()

         mantenimientos_buzos.fecha_lavado_celda= None #No aplica para lavado de celda
         mantenimientos_buzos.fecha_test_diagnostico= None #No aplica para test diagnostico
         mantenimientos_buzos.realizado_por = User.objects.get(username=request.user)
         mantenimientos_buzos.save()
         

     for id in mantenimientos_celdas_id:  #accion seleccionada lavado de celda
         mantenimientos_celdas=Lavado_buzo.objects.get(pk=id)
         mantenimientos_celdas.status_celda= Lavado_buzo.Status_celda.PROGRAMADO
         mantenimientos_celdas.fecha_lavado_celda= datetime.datetime.now() + datetime.timedelta(days=30)
         #mantenimientos_celdas.fecha_lavado_celda= Lavado_buzo.progrmado
         #mantenimientos_celdas.fecha_alerta_inferior_celda= Lavado_buzo.limite_inferior
         mantenimientos_celdas.fecha_alerta_inferior_celda= datetime.datetime.now() + datetime.timedelta(days=27) 
         #mantenimientos_celdas.fecha_alerta_superior_celda= Lavado_buzo.limite_superior
         mantenimientos_celdas.fecha_alerta_superior_celda= datetime.datetime.now() + datetime.timedelta(days=33)
         mantenimientos_celdas.save()
         mantenimientos_celdas.pk = None #Crea una copia 
         mantenimientos_celdas.status_celda= Lavado_buzo.Status_celda.REALIZADO
         mantenimientos_celdas.status= Lavado_buzo.Status.PENDIENTE
         mantenimientos_celdas.status_test= Lavado_buzo.Status_test.PENDIENTE
         mantenimientos_celdas.status_mantenimiento= Lavado_buzo.Status_mantenimiento.PENDIENTE
         mantenimientos_celdas.status_calificacion= Lavado_buzo.Status_calificacion.PENDIENTE
         
         mantenimientos_celdas.fecha_lavado_celda= datetime.datetime.now()
         #mantenimientos_celdas.fecha_lavado_celda= Lavado_buzo.date_joined
         mantenimientos_celdas.fecha_lavado_buzo= None #No aplica para el lavado de buzos
         mantenimientos_celdas.fecha_test_diagnostico= None #No aplica para test iagnostico
         mantenimientos_celdas.realizado_por_celda = User.objects.get(username=request.user)
         mantenimientos_celdas.save()

     for id in mantenimientos_test_id:  #accion seleccionada test de diagnostico
         mantenimientos_test=Lavado_buzo.objects.get(pk=id)
         mantenimientos_test.status_test= Lavado_buzo.Status_test.PROGRAMADO
         mantenimientos_test.fecha_test_diagnostico= datetime.datetime.now() + datetime.timedelta(days=30)
         #mantenimientos_test.fecha_test_diagnostico= Lavado_buzo.progrmado
         #mantenimientos_test.fecha_alerta_inferior_test= Lavado_buzo.limite_inferior
         mantenimientos_test.fecha_alerta_inferior_test= datetime.datetime.now() + datetime.timedelta(days=27) 
         #mantenimientos_test.fecha_alerta_superior_test= Lavado_buzo.limite_superior
         mantenimientos_test.fecha_alerta_superior_test= datetime.datetime.now() + datetime.timedelta(days=33)
         mantenimientos_test.save()
         mantenimientos_test.pk = None #Crea una copia 
         mantenimientos_test.status_test= Lavado_buzo.Status_test.REALIZADO
         mantenimientos_test.status= Lavado_buzo.Status.PENDIENTE
         mantenimientos_test.status_celda= Lavado_buzo.Status_celda.PENDIENTE
         mantenimientos_test.status_mantenimiento= Lavado_buzo.Status_mantenimiento.PENDIENTE
         mantenimientos_test.status_calificacion= Lavado_buzo.Status_calificacion.PENDIENTE
         mantenimientos_test.fecha_test_diagnostico= datetime.datetime.now()
         #mantenimientos_test.fecha_test_diagnostico= Lavado_buzo.date_joined
         mantenimientos_test.fecha_lavado_buzo= None #No aplica para el lavado de buzos
         mantenimientos_test.fecha_lavado_celda= None #No aplica para el lavado de celdas
         mantenimientos_test.realizado_por_test = User.objects.get(username=request.user)
         mantenimientos_test.save()

     for id in mantenimientos_preventivo:  
         mantenimientos_preventivo=Lavado_buzo.objects.get(pk=id)
         mantenimientos_preventivo.status_mantenimiento= Lavado_buzo.Status_mantenimiento.PROGRAMADO
         mantenimientos_preventivo.fecha_mantenimiento= datetime.datetime.now() +  relativedelta(months= 6)
         #mantenimientos_test.fecha_test_diagnostico= Lavado_buzo.progrmado
         #mantenimientos_test.fecha_alerta_inferior_test= Lavado_buzo.limite_inferior
         mantenimientos_preventivo.fecha_alerta_inferior_mantenimiento= datetime.datetime.now() + relativedelta(months= 5) 
         #mantenimientos_test.fecha_alerta_superior_test= Lavado_buzo.limite_superior
         mantenimientos_preventivo.fecha_alerta_superior_mantenimiento= datetime.datetime.now() + relativedelta(months= 7)
         mantenimientos_preventivo.save()
         mantenimientos_preventivo.pk = None #Crea una copia 
         mantenimientos_preventivo.status_mantenimiento= Lavado_buzo.Status_mantenimiento.REALIZADO
         mantenimientos_preventivo.status= Lavado_buzo.Status.PENDIENTE
         mantenimientos_preventivo.status_celda= Lavado_buzo.Status_celda.PENDIENTE
         mantenimientos_preventivo.status_test= Lavado_buzo.Status_test.PENDIENTE
         mantenimientos_preventivo.status_calificacion= Lavado_buzo.Status_calificacion.PENDIENTE
         
         mantenimientos_preventivo.fecha_mantenimiento= datetime.datetime.now()
         #mantenimientos_test.fecha_test_diagnostico= Lavado_buzo.date_joined
         mantenimientos_preventivo.fecha_lavado_buzo= None #No aplica para el lavado de buzos
         mantenimientos_preventivo.fecha_lavado_celda= None #No aplica para el lavado de celdas
         mantenimientos_preventivo.fecha_test_diagnostico= None #No aplica para el lavado de celdas
         mantenimientos_preventivo.realizado_por_mantenimiento = User.objects.get(username=request.user)
         #mantenimientos_preventivo.observaciones = User.objects.get(username=request.user)
         mantenimientos_preventivo.save()

     for id in calificacion_realizada:  
         calificacion=Lavado_buzo.objects.get(pk=id)
         calificacion.status_calificacion= Lavado_buzo.Status_calificacion.PROGRAMADO
         calificacion.fecha_calificacion= datetime.datetime.now() +  relativedelta(months= 6)
         #mantenimientos_test.fecha_test_diagnostico= Lavado_buzo.progrmado
         #mantenimientos_test.fecha_alerta_inferior_test= Lavado_buzo.limite_inferior
         calificacion.fecha_alerta_inferior_calificacion= datetime.datetime.now() + relativedelta(months= 5) 
         #mantenimientos_test.fecha_alerta_superior_test= Lavado_buzo.limite_superior
         calificacion.fecha_alerta_superior_calificacion= datetime.datetime.now() + relativedelta(months= 7)
         calificacion.save()
         calificacion.pk = None #Crea una copia 
         calificacion.status_calificacion= Lavado_buzo.Status_calificacion.REALIZADO
         calificacion.status= Lavado_buzo.Status.PENDIENTE
         calificacion.status_celda= Lavado_buzo.Status_celda.PENDIENTE
         calificacion.status_test= Lavado_buzo.Status_test.PENDIENTE
         calificacion.status_mantenimiento= Lavado_buzo.Status_mantenimiento.PENDIENTE
         
         calificacion.fecha_calificacion= datetime.datetime.now()
         #mantenimientos_test.fecha_test_diagnostico= Lavado_buzo.date_joined
         calificacion.fecha_lavado_buzo= None #No aplica para el lavado de buzos
         calificacion.fecha_lavado_celda= None #No aplica para el lavado de celdas
         calificacion.fecha_test_diagnostico= None #No aplica para el lavado de celdas
         calificacion.realizado_por_calificacion = User.objects.get(username=request.user)
         #mantenimientos_preventivo.observaciones = User.objects.get(username=request.user)
         calificacion.save()
         


   #print(date_joined)
   messages.success(request, "Registro actualizado exitosamente")
   return redirect("mantenimientos_periodicos")

def cambiar_estado_secuencias(request):
   if request.method=="POST":
     estado_impresion=request.POST.getlist("imprimir")
     estado_reporte=request.POST.getlist("reportar")
     estado_auditar=request.POST.getlist("auditar")

     for id in estado_impresion: 
         impresion=Secuencias.objects.get(pk=id)
         impresion.status= Secuencias.Status.IMPRESA
       
         impresion.imprimir = str(User.objects.get(username=request.user)) #usuario que imprime
         impresion.fecha_impresion= datetime.datetime.now()
         impresion.save()
     for id in estado_reporte:
         reporte=Secuencias.objects.get(pk=id) 
         reporte.status=Secuencias.Status.REPORTADA
         reporte.reportar= str(User.objects.get(username=request.user)) #usuario que reporta
         reporte.fecha_reporte=datetime.datetime.now()
         reporte.save()

     for id in estado_auditar:
         audit=Secuencias.objects.get(pk=id)
         audit.status=Secuencias.Status.AUDITADA
         audit.auditar= str(User.objects.get(username=request.user)) #usuario que audita
         audit.fecha_auditada=datetime.datetime.now()
         audit.save()    

   messages.success(request, "Registro actualizado exitosamente")
   return redirect("proceso_secuencias_en_curso")

def cambiar_estado_validada_revisada(request):
   if request.method=="POST":
     estado_validar=request.POST.getlist("validar_revisar")
     estado_invalidar=request.POST.getlist("problemas_equipo_1")
     estado_invalidar_1=request.POST.getlist("problemas_equipo_2")
     estado_invalidar_2=request.POST.getlist("problemas_columna")
     estado_invalidar_3=request.POST.getlist("incumplimientoSST1")
     estado_invalidar_4=request.POST.getlist("incumplimientoSST2")
     estado_invalidar_5=request.POST.getlist("incumplimientoSST3")
     estado_invalidar_6=request.POST.getlist("problemas_de_FM")
     estado_invalidar_7=request.POST.getlist("Problemas_de_red")
     estado_invalidar_8=request.POST.getlist("falla__fluido_electrico")
     estado_invalidar_9=request.POST.getlist("otros")
     for id in estado_validar: 
         validar=Secuencias.objects.get(pk=id)
         validar.status= Secuencias.Status.REVISADA
         validar.validar = str(User.objects.get(username=request.user)) #usuario que valida
         validar.fecha_validar= datetime.datetime.now()
         validar.fecha_invalidar = "0001-01-01"
         validar.save()
     for id in estado_invalidar: 
         estado_invalidar=Secuencias.objects.get(pk=id)
         estado_invalidar.status= Secuencias.Status.INVALIDA
         estado_invalidar.invalidar =  str(User.objects.get(username=request.user)) #usuario que invalida
         estado_invalidar.fecha_invalidar= datetime.datetime.now()
         estado_invalidar.invalidar_Secuencia= Secuencias.Invalidar_Secuencia.PROBLEMAS_EQUIPO_1
         estado_invalidar.save()
     for id in estado_invalidar_1: 
         estado_invalidar=Secuencias.objects.get(pk=id)
         estado_invalidar.status= Secuencias.Status.INVALIDA
         estado_invalidar.invalidar =  str(User.objects.get(username=request.user)) #usuario que invalida
         estado_invalidar.fecha_invalidar= datetime.datetime.now()
         estado_invalidar.invalidar_Secuencia= Secuencias.Invalidar_Secuencia.PROBLEMAS_EQUIPO_2
         estado_invalidar.save()
     for id in estado_invalidar_2: 
         estado_invalidar=Secuencias.objects.get(pk=id)
         estado_invalidar.status= Secuencias.Status.INVALIDA
         estado_invalidar.invalidar =  str(User.objects.get(username=request.user)) #usuario que invalida
         estado_invalidar.fecha_invalidar= datetime.datetime.now()
         estado_invalidar.invalidar_Secuencia= Secuencias.Invalidar_Secuencia.PROBLEMAS_COLUMNA
         estado_invalidar.save()
     for id in estado_invalidar_3: 
         estado_invalidar=Secuencias.objects.get(pk=id)
         estado_invalidar.status= Secuencias.Status.INVALIDA
         estado_invalidar.invalidar =  str(User.objects.get(username=request.user)) #usuario que invalida
         estado_invalidar.fecha_invalidar= datetime.datetime.now()
         estado_invalidar.invalidar_Secuencia= Secuencias.Invalidar_Secuencia.INCUMPLIMIENTO_SST_1
         estado_invalidar.save()
     for id in estado_invalidar_4: 
         estado_invalidar=Secuencias.objects.get(pk=id)
         estado_invalidar.status= Secuencias.Status.INVALIDA
         estado_invalidar.invalidar =  str(User.objects.get(username=request.user)) #usuario que invalida
         estado_invalidar.fecha_invalidar= datetime.datetime.now()
         estado_invalidar.invalidar_Secuencia= Secuencias.Invalidar_Secuencia.INCUMPLIMIENTO_SST_2
         estado_invalidar.save()
     for id in estado_invalidar_5: 
         estado_invalidar=Secuencias.objects.get(pk=id)
         estado_invalidar.status= Secuencias.Status.INVALIDA
         estado_invalidar.invalidar =  str(User.objects.get(username=request.user)) #usuario que invalida
         estado_invalidar.fecha_invalidar= datetime.datetime.now()
         estado_invalidar.invalidar_Secuencia= Secuencias.Invalidar_Secuencia.INCUMPLIMIENTO_SST_3
         estado_invalidar.save()
     for id in estado_invalidar_6: 
         estado_invalidar=Secuencias.objects.get(pk=id)
         estado_invalidar.status= Secuencias.Status.INVALIDA
         estado_invalidar.invalidar =  str(User.objects.get(username=request.user)) #usuario que invalida
         estado_invalidar.fecha_invalidar= datetime.datetime.now()
         estado_invalidar.invalidar_Secuencia= Secuencias.Invalidar_Secuencia.PROBLEMAS_FM
         estado_invalidar.save()
     for id in estado_invalidar_7: 
         estado_invalidar=Secuencias.objects.get(pk=id)
         estado_invalidar.status= Secuencias.Status.INVALIDA
         estado_invalidar.invalidar =  str(User.objects.get(username=request.user)) #usuario que invalida
         estado_invalidar.fecha_invalidar= datetime.datetime.now()
         estado_invalidar.invalidar_Secuencia= Secuencias.Invalidar_Secuencia.PROBLEMAS_RED
         estado_invalidar.save()
     for id in estado_invalidar_8: 
         estado_invalidar=Secuencias.objects.get(pk=id)
         estado_invalidar.status= Secuencias.Status.INVALIDA
         estado_invalidar.invalidar =  str(User.objects.get(username=request.user)) #usuario que invalida
         estado_invalidar.fecha_invalidar= datetime.datetime.now()
         estado_invalidar.invalidar_Secuencia= Secuencias.Invalidar_Secuencia.PROBLEMAS_FE
         estado_invalidar.save()
     for id in estado_invalidar_9: 
         estado_invalidar=Secuencias.objects.get(pk=id)
         estado_invalidar.status= Secuencias.Status.INVALIDA
         estado_invalidar.invalidar =  str(User.objects.get(username=request.user)) #usuario que invalida
         estado_invalidar.fecha_invalidar= datetime.datetime.now()
         estado_invalidar.invalidar_Secuencia= Secuencias.Invalidar_Secuencia.OTROS
         estado_invalidar.save()
   messages.success(request, "Registro actualizado exitosamente")
   return redirect("crear_secuencias_en_curso")
   
