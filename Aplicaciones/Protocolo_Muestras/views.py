from django.shortcuts import render, redirect
from .models import Proceso
from Aplicaciones.Secuencias.models import Secuencias
from .forms import ProcesoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def protocolo_proceso(request):
    titulo = "Protocolo de Métodos"
    protocolo_proceso=Proceso.objects.all()
    #secuencia_registro = Secuencias.objects.filter(status="Registrada").count()
    
    context = {

        "titulo": titulo,
        "protocolo_proceso": protocolo_proceso,
       
        #"crear_metodologia":crear_metodologia,
        #"secuencia_registro":secuencia_registro,
    }
    return render(request, "protocolo_proceso/protocolo_proceso.html", context)


@login_required
def crear_protocolo_proceso(request):
    titulo="Crear Protocolos de Proceso"
    protocolo_proceso=Proceso.objects.all()
   
    if request.method == "POST":
        form = ProcesoForm(request.POST or None)
       
        if form.is_valid():
            form.save()

            messages.success(request, "Protocolo creado satisfactoriamente")
            return redirect("protocolo_proceso")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
             #return redirect("crear_protocolo_metodos")
    else:
            
        form = ProcesoForm() 
    context={
        "titulo":titulo,
        "form":form,
        "protocolo_proceso":protocolo_proceso
    }
    return render(request, "protocolo_proceso/crear_protocolo_proceso.html", context)

@login_required
def editar_protocolo_proceso(request, pk):

    titulo="Editar Protocolos"
    protocolo_proceso=Proceso.objects.get(id=pk)
    protocolo_proceso_iterar=Proceso.objects.all()

    if request.method == "POST":
         form = ProcesoForm(request.POST, instance=protocolo_proceso)
         #messages.success(request, "Editada con exito")
         if form.is_valid():
           form.save()
           messages.success(request, "Protocolo editado correctamente")
           return redirect("protocolo_proceso")
         else:
           messages.error(request, "Por favor revisa los datos ingresados")  
    else:
          form = ProcesoForm(instance=protocolo_proceso)
    context={
    "titulo":titulo,
    "form":form,
    "protocolo_proceso": protocolo_proceso,
    "protocolo_proceso_iterar":protocolo_proceso_iterar
   
}
    return render(request, "protocolo_proceso/edicion_protocolo_proceso.html", context)

@login_required
def revisar_protocolo_proceso(request, pk):

    titulo="Revisar Protocolos"
    protocolo_metodo=Proceso.objects.get(id=pk)
    pkt = Proceso.objects.filter(id=pk)
    a=2
    secuencias1=Secuencias.objects.filter(protocolo_proceso=pk)
    status_secuencia=Secuencias.objects.filter(status=pk)
    contarParametroProtocolo=Proceso.objects.values("muestras").filter(id=pk).count()
     
    contarStatusRegistrada=Secuencias.objects.filter(protocolo_proceso=pk, status="Registrada").count()
    contarStatusRevisada=Secuencias.objects.filter(protocolo_proceso=pk, status="Revisada").count()
    contarStatusImpresa=Secuencias.objects.filter(protocolo_proceso=pk, status="Impresa").count()
    contarStatusReportada=Secuencias.objects.filter(protocolo_proceso=pk, status="Reportada").count()
    contarStatusAuditada=Secuencias.objects.filter(protocolo_proceso=pk, status="Auditada").count()

    porcentajeStatusRegistrada=contarStatusRegistrada*20/contarParametroProtocolo
    porcentajeStatusRevisada=contarStatusRevisada*40/contarParametroProtocolo
    porcentajeStatusImpresa=contarStatusImpresa*60/contarParametroProtocolo
    porcentajeStatusReportada=contarStatusReportada*80.0/contarParametroProtocolo
    porcentajeStatusAuditada=contarStatusAuditada*100/contarParametroProtocolo

    labels = []
    data = []

    queryset = Secuencias.objects.order_by('-nombre')[:5]
    for city in queryset:
        labels.append(city.nombre)
        data.append(city.nombre)
  
    context={
         
        "titulo":titulo,
   
    "protocolo_metodo": protocolo_metodo,
    "pkt":pkt,
    "secuencias1":secuencias1,
    "status_secuencia":status_secuencia,
    "labels":labels,
    "data":data,
    "queryset":queryset,
    "contarParametroProtocolo":contarParametroProtocolo,
    "a":a,
    "contarStatusRegistrada":contarStatusRegistrada,
    "contarStatusRevisada":contarStatusRevisada,
    "contarStatusImpresa":contarStatusImpresa,
    "contarStatusReportada":contarStatusReportada,
    "contarStatusAuditada":contarStatusAuditada,
    "porcentajeStatusRegistrada":porcentajeStatusRegistrada,
    "porcentajeStatusRevisada":porcentajeStatusRevisada,
    "porcentajeStatusImpresa":porcentajeStatusImpresa,
    "porcentajeStatusReportada":porcentajeStatusReportada,
    "porcentajeStatusAuditada":porcentajeStatusAuditada,
   

}
    return render(request, "protocolo_proceso/revisar_protocolo_proceso.html", context)

