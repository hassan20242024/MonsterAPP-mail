from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Aplicaciones.Protocolo_Metodos.models import Protocolos
from Aplicaciones.Protocolo_Muestras.models import Proceso
from django.db.models import Count,Q,Sum
import json
import datetime
from django.conf import settings
settings.DATE_FORMAT
from django.template.defaultfilters import date



# Create your views here.

 
        


def inicio(request):
    context={
    }
    return render(request, "index-admin.html", context)

@login_required
def inicioAdmin(request):
  

    
     return render(request, "index-admin.html")


@login_required
def adm_inicio(request):
     #GRAFICO PARA PROTOCOLOS DE METODOS FINALIZADOS
     registro_total_protocolo_metodos = Protocolos.objects.count()
     
     #registro_total_protocolo_metodos_reales= registro_total_protocolo_metodos - 1
     dataset = Protocolos.objects \
       .values('fecha_final__month')\
        .annotate(Finalizado=Count('fecha_final__month', filter=Q(estado_protocolo="6", fecha_final__year=2024)),
                 ) 
     #GRAFICO PARA PROTOCOLOS DE PROCESO FINALIZADOS
     registro_total_protocolo_proceso = Proceso.objects.count()
     #registro_total_protocolo_proceso_reales= registro_total_protocolo_proceso - 1
     datasetPr = Proceso.objects \
       .values('fecha_final__month')\
        .annotate(Finalizado=Count('fecha_final__month', filter=Q(estado_del_proceso="6", fecha_final__year=2024)),
                 )              
#extra(select={'month': 'DATE_FORMAT(date, '%B')'})
        #.order_by('-fecha_final__month')
   #fecha = datetime.datetime.strptime(dataset, "%d/%m/%Y").strftime("%Y-%m-%d")

     #categories = []
     #Finalizado = list()
  
     #for entry in dataset:
        ##Finalizado.append(entry['Finalizado'])
     #Finalizado_series = {
        #'name': 'Finalizado',
        #'data': Finalizado,
        #'colorByPoint': 'True',
        #'showInLegen': 'False',
        
   ###'chart': {'type': 'column' },
        #'title': {'text': ''},
        #'xAxis': [
            #{'categories': categories},
        #],
        #'series': [Finalizado_series],
    #}
     #chart1 = {
        #'chart': {'type': 'line' },
        #'title': {'text': ''},
        #'xAxis': {'categories': categories},
        #'series': [Finalizado_series]
    #}

     #dump = json.dumps(chart)
     #dump1 = json.dumps(chart1)

     dataset_motivo = Protocolos.objects.values("estado_protocolo__estado_motivo").annotate(
          ejecucion=Count("estado_protocolo__estado_motivo", filter=Q(estado_protocolo="1")),
            falta_insumos=Count("estado_protocolo__estado_motivo", filter=Q(estado_protocolo="2")),
             metodologia=Count("estado_protocolo__estado_motivo", filter=Q(estado_protocolo="3")),
                 criterio=Count("estado_protocolo__estado_motivo", filter=Q(estado_protocolo="4")),
         Listado=Count("estado_protocolo__estado_motivo", filter=Q(estado_protocolo="5")),
         finalizado=Count("estado_protocolo__estado_motivo", filter=Q(estado_protocolo="6")),
       
        
     
        
     ).exclude(estado_protocolo="7")
     categories = []
     ejecucion = list()
     falta_insumos = list()
     metodologia = list()
       
     criterio = list()
     Listado = list()
     finalizado = list()
 
   
     for entry in dataset_motivo:
         categories.append('%s ' % entry['estado_protocolo__estado_motivo'])
         ejecucion.append(entry['ejecucion'])
         falta_insumos.append(entry['falta_insumos'])
         metodologia.append(entry['metodologia'])
         criterio.append(entry['criterio'])
         Listado.append(entry['Listado'])
         finalizado.append(entry['finalizado'])
        
     ejecucion_series = {
        'name': 'En ejecución',
        'data': ejecucion,
        'color': '#308034', 

    }
     falta_insumos_series = {
        'name': 'Falta de insumos',
        'data': falta_insumos,
        'color': '#11d0d2',
    } 
     metodologia_series = {
        'name': 'Problemas de método',
        'data': metodologia,
        'color': '#fdbb30',
    } 
     criterio_series = {
        'name': 'Muestras no cumplen parámetros',
        'data': criterio,
        'color': '#ff0d0d',
    }      
     listadoseries = {
        'name': 'Listado',
        'data': Listado,
        'color': '#a6a685',
   } 
     finalizado_series = {
        'name': 'Finalizado',
        'data': finalizado,
        'color': '#1aa1c0',
   } 

    
    
     chart2 = {
        'chart': {'type': 'bar'},
        'title': {'text': ''},
         "credits": "false",
         
         
        'xAxis': {'categories': categories},
        'series': [ejecucion_series,falta_insumos_series,metodologia_series,criterio_series,   listadoseries,finalizado_series,],
          "plotOptions": {
		"bar": {
			
			"pointPadding": -1.9,
			"borderWidth": 10
		}
	},
    } 
    
     dump2 = json.dumps(chart2)   
     titulo="Tablero principal"

     #GRAFICO PARA ESTADO DE PROTOCOLOS DE PROCESO 
     dataset_motivo = Proceso.objects.values("estado_del_proceso__estado_motivo").annotate(
         Listado=Count("estado_del_proceso", filter=Q(estado_del_proceso="5")),
         finalizado=Count("estado_del_proceso", filter=Q(estado_del_proceso="6")),
         falta_insumos=Count("estado_del_proceso__estado_motivo", filter=Q(estado_del_proceso="2")),
         metodologia=Count("estado_del_proceso__estado_motivo", filter=Q(estado_del_proceso="3")),
         criterio=Count("estado_del_proceso__estado_motivo", filter=Q(estado_del_proceso="4")),
         ejecucion=Count("estado_del_proceso", filter=Q(estado_del_proceso="1"))
     ).exclude(estado_del_proceso="7")
     categories = []
     Listado = list()
     finalizado = list()
     falta_insumos = list()
     metodologia = list()
     criterio = list()
     ejecucion = list()
     for entry in dataset_motivo:
         categories.append('%s ' % entry['estado_del_proceso__estado_motivo'])
         Listado.append(entry['Listado'])
         finalizado.append(entry['finalizado'])
         falta_insumos.append(entry['falta_insumos'])
         metodologia.append(entry['metodologia'])
         criterio.append(entry['criterio'])
         ejecucion.append(entry['ejecucion'])
     listadoseries = {
        'name': 'Listado',
        'data': Listado,
        'color': '#a6a685',
   } 
     finalizado_series = {
        'name': 'Finalizado',
        'data': finalizado,
        'color': '#1aa1c0',
   } 

     falta_insumos_series = {
        'name': 'Falta de insumos',
        'data': falta_insumos,
        'color': '#11d0d2',
    } 
     metodologia_series = {
        'name': 'Problemas de método',
        'data': metodologia,
        'color': '#fdbb30',
    } 
     criterio_series = {
        'name': 'Muestras no cumplen parámetros',
        'data': criterio,
        'color': '#f34235',
    } 
     ejecucion_series = {
        'name': 'En ejecución',
        'data': ejecucion,
        'color': '#308034', 
    } 
     chart3 = {
        'chart': {'type': 'bar'},
        'title': {'text': ''},
         "credits": "false",
        
        'xAxis': {'categories': categories},
        'series': [falta_insumos_series,finalizado_series,metodologia_series,criterio_series,listadoseries,ejecucion_series],
        "plotOptions": {
		"bar": {
			
			"pointPadding": -1.9,
			"borderWidth": 10
		}
	},
    } 
     dump3 = json.dumps(chart3)   
     titulo="Tablero principal"


     context={
        "titulo":titulo,
       # 'chart': dump,
        #'chart1': dump1,
        "dataset":dataset,
         "datasetPr":datasetPr,
        #"Finalizado":Finalizado,
        'chart2': dump2,
        'chart3': dump3,
        "registro_total_protocolo_metodos":registro_total_protocolo_metodos,
        "registro_total_protocolo_proceso":registro_total_protocolo_proceso,
        #"registro_total_protocolo_metodos_reales":registro_total_protocolo_metodos_reales,
        #"registro_total_protocolo_proceso_reales":registro_total_protocolo_proceso_reales

    }
     
     return render(request, "inicio.html", context)

