from django.shortcuts import render, redirect

from .models import Protocolos,Subparametro, Parametro, Metodologia,EstadoProtocolo,Viabilidad,Titulo_Parametro,Celda,Muestras_y_Placebos,Ensayo, Cliente, Celda, Metodo, Tipo_muestra, Etapa
from Aplicaciones.Secuencias.models import Sistema
from Aplicaciones.Protocolo_Muestras.models import ViabilidadProceso
from django.contrib.auth.models import User
from .forms import ProtocolosForm,ParametroForm, MetodologiaForm, EstadoProtocoloForm, crear_ensayoForm,ViabilidadForm,sistemaForm, SubparametroForm,Titulo_ParametroForm, ingresar_muestrasForm, clienteForm, CeldaForm, MetodoForm, tipo_muestrasForm, EtapaForm, viavilidad_procesoForm
from Aplicaciones.Secuencias.models import Secuencias
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def protocolo_metodos(request):
    titulo = "Protocolo de Métodos"
    protocolo_metodos=Protocolos.objects.all()
    #secuencia_registro = Secuencias.objects.filter(status="Registrada").count()
    
    context = {

        "titulo": titulo,
        "protocolo_metodos": protocolo_metodos,
       
        "crear_metodologia":crear_metodologia,
        #"secuencia_registro":secuencia_registro,
    }
    return render(request, "protocolo_metodos/protocolo_metodos.html", context)

@login_required
def crear_protocolo_metodos(request):
    titulo="Crear Protocolos"
    protocolo_metodos=Protocolos.objects.all()
   
    if request.method == "POST":
        form = ProtocolosForm(request.POST or None)
       
        if form.is_valid():
            form.save()

            messages.success(request, "Protocolo creado satisfactoriamente")
           
            return redirect("protocolo_metodos")
        else:
             messages.error(request, "Por favor, revisa los datos ingresados")
             #return redirect("crear_protocolo_metodos")
    else:
            
        form = ProtocolosForm() 
        
    context={
        "titulo":titulo,
        "form":form,
        
        
        "protocolo_metodos":protocolo_metodos
    }
    return render(request, "protocolo_metodos/crear_protocolo_metodos.html", context)

@login_required
def configuracion_protocolo_metodos(request):
    titulo = "Ajustes Protocolo de Métodos/Parámetros"
    Pto=Parametro.objects.all()
    tituloParametro=Titulo_Parametro.objects.all()
    nombreSubparametro=Subparametro.objects.all()

    if request.method == "POST":
        form = ParametroForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("configuracion_protocolo_metodos")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = ParametroForm() 
    
    context={
        "titulo":titulo,
        "form":form,
       "Pto": Pto,
       "tituloParametro":tituloParametro,
       "nombreSubparametro":nombreSubparametro
    }
   
    return render(request, "protocolo_metodos/configuracion_protocolo_metodos.html", context)

@login_required
def editar_protocolo_metodos(request, pk):
    titulo="Editar Protocolos"
    protocolo_metodo=Protocolos.objects.get(id=pk)
    protocolo_metodos=Protocolos.objects.all()

    if request.method == "POST":
         form = ProtocolosForm(request.POST, instance=protocolo_metodo)
         #messages.success(request, "Editada con exito")
         if form.is_valid():
           form.save()
           messages.success(request, "Protocolo editado correctamente")
           return redirect("protocolo_metodos")
         else:
           messages.error(request, "Por favor revisa los datos ingresados")  
    else:
          form = ProtocolosForm(instance=protocolo_metodo)
    context={
    "titulo":titulo,
    "form":form,
    "protocolo_metodo": protocolo_metodo,
    "protocolo_metodos":protocolo_metodos
   
}
    return render(request, "protocolo_metodos/edicion_protocolo_metodos.html", context)

@login_required
def revisar_protocolo_metodos(request, pk):

    titulo="Revisar Protocolos"
    protocolo_metodo=Protocolos.objects.get(id=pk)
    pkt = Protocolos.objects.filter(id=pk)
    a=2
    secuencias1=Secuencias.objects.filter(protocolo=pk)
    status_secuencia=Secuencias.objects.filter(status=pk)
    contarParametroProtocolo=Protocolos.objects.values("parametro").filter(id=pk).count()
     
    contarStatusRegistrada=Secuencias.objects.filter(protocolo=pk, status="Registrada").count()
    contarStatusRevisada=Secuencias.objects.filter(protocolo=pk, status="Revisada").count()
    contarStatusImpresa=Secuencias.objects.filter(protocolo=pk, status="Impresa").count()
    contarStatusReportada=Secuencias.objects.filter(protocolo=pk, status="Reportada").count()
    contarStatusAuditada=Secuencias.objects.filter(protocolo=pk, status="Auditada").count()

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
    return render(request, "protocolo_metodos/revisar_protocolo_metodos.html", context)

@login_required
def editar_parametro(request, pk):
    titulo="Editar Parámetros"
   
   
    if request.method == "POST":
        Pto=Parametro.objects.get(pk=pk)
        form = ParametroForm(request.POST, instance=Pto)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("configuracion_protocolo_metodos")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = ParametroForm(instance=Pto)

    context={
        "titulo":titulo,
        "form":form,
        "Pto":Pto
    }
    return render(request, "protocolo_metodos/configuracion_protocolo_metodos.html", context)

@login_required
def subparametro(request):
    titulo="Ajustes Protocolo de Métodos/Subparametros"
    subparametro=Subparametro.objects.all()
    
    if request.method == "POST":
        form = SubparametroForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("subparametro")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = SubparametroForm() 
    context={
        "titulo":titulo,
        "form":form,
        "subparametro":subparametro
    }
    return render(request, "protocolo_metodos/subparametro.html", context)

@login_required
def editar_subparametro(request, pk):
    titulo="Ajustes Protocolo de Métodos/Subparametros"
    subparametro=Subparametro.objects.get(id=pk)
    
    if request.method == "POST":
        form = SubparametroForm(request.POST, instance=subparametro)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("subparametro")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = SubparametroForm(instance=subparametro) 
    context={
        "titulo":titulo,
        "form":form,
        "subparametro":subparametro
    }
    return render(request, "protocolo_metodos/subparametro.html", context)

@login_required
def titulo_parametro(request):
    titulo="Ajustes Protocolo de Métodos/Titulo parámetro"
    titulo_parametro=Titulo_Parametro.objects.all()
    
    if request.method == "POST":
        form = Titulo_ParametroForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("titulo_parametro")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = Titulo_ParametroForm() 
    context={
        "titulo":titulo,
        "form":form,
        "titulo_parametro":titulo_parametro
    }
    return render(request, "protocolo_metodos/titulo_parametro.html", context)

@login_required
def editar_titulo_parametro(request, pk):
    titulo="Editar Título Parámetro"
    titulo_parametro=Titulo_Parametro.objects.get(id=pk)
   
    if request.method == "POST":
        form = Titulo_ParametroForm(request.POST, instance=titulo_parametro)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("titulo_parametro")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = Titulo_ParametroForm(instance=titulo_parametro)

    context={
        "titulo":titulo,
        "form":form,
        "titulo_parametro":titulo_parametro
    }
    return render(request, "protocolo_metodos/titulo_parametro.html", context)

@login_required
def crear_metodologia(request):
    titulo="Ajustes Protocolo de Métodos/Metodologia"
    crear_metodologia=Metodologia.objects.all()
    
    
    if request.method == "POST":
        form = MetodologiaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("crear_metodologia")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = MetodologiaForm() 
    context={
        "titulo":titulo,
        "form":form,
        "crear_metodologia":crear_metodologia
    }
    return render(request, "protocolo_metodos/crear_metodologia.html", context)

@login_required
def editar_metodologia(request, pk):
    titulo="Ajustes Protocolo de Métodos/Metodologia"
    crear_metodologia=Metodologia.objects.get(id=pk)
    
    
    if request.method == "POST":
        form = MetodologiaForm(request.POST, instance=crear_metodologia)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("crear_metodologia")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = MetodologiaForm(instance=crear_metodologia) 
    context={
        "titulo":titulo,
        "form":form,
        "crear_metodologia":crear_metodologia
    }
    return render(request, "protocolo_metodos/crear_metodologia.html", context)

@login_required
def definir_estado(request):
    titulo="Ajustes Protocolo de Métodos/Estado"
    definir_estado=EstadoProtocolo.objects.all()
    
    
    if request.method == "POST":
        form = EstadoProtocoloForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("definir_estado")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = EstadoProtocoloForm() 
    context={
        "titulo":titulo,
        "form":form,
        "definir_estado":definir_estado
    }
    return render(request, "protocolo_metodos/definir_estado.html", context)

@login_required
def editar_definir_estado(request,pk):
    titulo="Ajustes Protocolo de Métodos/Estado"
    definir_estado=EstadoProtocolo.objects.get(id=pk)
    
    
    if request.method == "POST":
        form = EstadoProtocoloForm(request.POST, instance=definir_estado)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("definir_estado")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = EstadoProtocoloForm(instance=definir_estado) 
    context={
        "titulo":titulo,
        "form":form,
        "definir_estado":definir_estado
    }
    return render(request, "protocolo_metodos/definir_estado.html", context)

@login_required
def crear_ensayo(request):
    titulo="Ajustes Protocolo de Métodos/Ensayo"
    crear_ensayo=Ensayo.objects.all()
    if request.method == "POST":
        form = crear_ensayoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("crear_ensayo")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = crear_ensayoForm() 
    context={
        "titulo":titulo,
        "form":form,
        "crear_ensayo":crear_ensayo,
        
    }
    return render(request, "protocolo_metodos/crear_ensayo.html", context)

@login_required
def editar_ensayo(request, pk):
    titulo="Ajustes Protocolo de Métodos/Ensayo"
    crear_ensayo=Ensayo.objects.get(id=pk)
    if request.method == "POST":
        form = crear_ensayoForm(request.POST, instance=crear_ensayo)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("crear_ensayo")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = crear_ensayoForm(instance=crear_ensayo) 
    context={
        "titulo":titulo,
        "form":form,
        "crear_ensayo":crear_ensayo,
        
    }
    return render(request, "protocolo_metodos/crear_ensayo.html", context)

@login_required
def insumosDelProceso(request):
    titulo="Ajustes Protocolo de Métodos/Insumos del Proceso"
    viabilidad=Viabilidad.objects.all()
    
    
    if request.method == "POST":
        form = ViabilidadForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("insumosDelProceso")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = ViabilidadForm() 
    context={
        "titulo":titulo,
        "form":form,
        "viabilidad":viabilidad
    }
    return render(request, "protocolo_metodos/insumosDelProceso.html", context)

@login_required
def editar_insumosDelProceso(request, pk):
    titulo="Ajustes Protocolo de Métodos/Insumos del Proceso"
    viabilidad=Viabilidad.objects.get(id=pk)
    
    
    if request.method == "POST":
        form = ViabilidadForm(request.POST, instance=viabilidad)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("insumosDelProceso")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = ViabilidadForm(instance=viabilidad) 
    context={
        "titulo":titulo,
        "form":form,
        "viabilidad":viabilidad
    }
    return render(request, "protocolo_metodos/insumosDelProceso.html", context)

@login_required
def crear_cliente(request):
    titulo="Ajustes Protocolo de Métodos/Clientes"
    crear_cliente=Cliente.objects.all()
    if request.method == "POST":
        form = clienteForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("crear_cliente")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = clienteForm() 
    context={
        "titulo":titulo,
        "form":form,
        "crear_cliente":crear_cliente,
        
    }
    return render(request, "protocolo_metodos/clientes.html", context)

    
@login_required
def editar_cliente(request, pk):
    titulo="Ajustes Protocolo de Métodos/Clientes"
    crear_cliente=Cliente.objects.get(id=pk)
    if request.method == "POST":
        form = clienteForm(request.POST, instance=crear_cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("crear_cliente")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = clienteForm(instance=crear_cliente) 
    context={
        "titulo":titulo,
        "form":form,
        "crear_cliente":crear_cliente,
        
    }
    return render(request, "protocolo_metodos/clientes.html", context)

@login_required
def detalles_protocolo_metodos(request):
    titulo = "Detalles del Protocolo"
    protocolo_metodos=Protocolos.objects.all()
    
    context = {

        "titulo": titulo,
        "protocolo_metodos": protocolo_metodos,
       
    }

    return render(request, "protocolo_metodos/detalles_protocolo_metodos.html", context)

@login_required
def muestras(request):
    titulo = "Muestras de Análisis"
    muestras=Muestras_y_Placebos.objects.all()
    #secuencia_registro = Secuencias.objects.filter(status="Registrada").count()
    context = {

        "titulo": titulo,
        "muestras": muestras,
    }
    return render(request, "protocolo_metodos/muestras.html", context)

@login_required
def ingresar_muestras(request):
    titulo="Ingreso de Muestras"
    ingresar_muestras=Muestras_y_Placebos.objects.all()
    
    
    if request.method == "POST":
        form = ingresar_muestrasForm(request.POST or None)
     
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("muestras")
        else:
             messages.error(request, "Por favor revisa los datos ingresados; quizas le falta diligenciar un campo o los campos Lote y Etapa, coinciden con otro registro") 
    else:
        form = ingresar_muestrasForm() 
    context={
        "titulo":titulo,
        "form":form,
        "ingresar_muestras":ingresar_muestras
    }

    return render(request, "protocolo_metodos/ingresar_muestras.html", context)

@login_required
def editar_muestras(request, pk):
    titulo="Editar Muestras"
    muestra=Muestras_y_Placebos.objects.get(id=pk)
    muestras=Muestras_y_Placebos.objects.all()

    if request.method == "POST":
         form = ingresar_muestrasForm(request.POST, instance=muestra)
         #messages.success(request, "Editada con exito")
         if form.is_valid():
           form.save()
           messages.success(request, "Registro editado correctamente")
           return redirect("muestras")
         else:
           messages.error(request, "Por favor revisa los datos ingresados; quizas le falta diligenciar un campo o los campos Lote y Etapa, coinciden con otro registro")  
    else:
          form = ingresar_muestrasForm(instance=muestra)
    context={
    "titulo":titulo,
    "form":form,
    "protocolo_metodo": muestra,
    "protocolo_metodos":muestras,
   
}
    return render(request, "protocolo_metodos/editar_muestras.html", context)

@login_required
def duplicar_muestras(request, pk):
    titulo="Duplicar Muestras"
    muestra=Muestras_y_Placebos.objects.get(id=pk)
    muestras=Muestras_y_Placebos.objects.all()

    if request.method == "POST":
         form = ingresar_muestrasForm(request.POST)
         #messages.success(request, "Editada con exito")
         if form.is_valid():
           form.save()
           messages.success(request, "Registro creado correctamente")
           return redirect("muestras")
         else:
           messages.error(request, "Por favor revisa los datos ingresados; quizas le falta diligenciar un campo o los campos Lote y Etapa, coinciden con otro registro")  
    else:
          form = ingresar_muestrasForm(instance=muestra)
    context={
    "titulo":titulo,
    "form":form,
    "protocolo_metodo": muestra,
    "protocolo_metodos":muestras,
   
}
    return render(request, "protocolo_metodos/duplicar_muestras.html", context)

@login_required
def sistemas(request):
    titulo="Sistemas"
    sistemas=Sistema.objects.all()
    if request.method == "POST":
        form = sistemaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Sistema creado satisfactoriamente")
            return redirect("sistemas")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = sistemaForm() 
    context={
        "titulo":titulo,
        "form":form,
        "sistemas":sistemas,
        
    }
    return render(request, "protocolo_metodos/crear_sistemas.html", context)

@login_required
def editar_sistemas(request, pk):
    titulo="Editar Sistemas"
    sistemas=Sistema.objects.get(id=pk)
    if request.method == "POST":
        form = sistemaForm(request.POST, instance=sistemas)
        if form.is_valid():
            form.save()
            messages.success(request, "Sistema editado satisfactoriamente")
            return redirect("sistemas")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = sistemaForm(instance=sistemas) 
    context={
        "titulo":titulo,
        "form":form,
        "crear_cliente":crear_cliente,
        
    }
    return render(request, "protocolo_metodos/crear_sistemas.html", context)



@login_required
def celdas(request):
    titulo="Celdas"
    celdas=Celda.objects.all()
    responsable = User.objects.all
    if request.method == "POST":
        form = CeldaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Celda creada satisfactoriamente")
            return redirect("celdas")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = CeldaForm() 
    context={
        "titulo":titulo,
        "form":form,
        "celdas":celdas,
        "responsable":responsable,
        
    }
    return render(request, "protocolo_metodos/celdas.html", context)

@login_required
def editar_celdas(request, pk):
    titulo="Editar Celdas"
    responsable = User.objects.all
    celdas=Celda.objects.get(id=pk)
    if request.method == "POST":
        form = CeldaForm(request.POST, instance=celdas)
        if form.is_valid():
            form.save()
            messages.success(request, "Celda editada satisfactoriamente")
            return redirect("celdas")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = CeldaForm(instance=celdas) 
    context={
        "titulo":titulo,
        "form":form,
        "celdas":celdas,
        responsable:responsable,
        
    }
    return render(request, "protocolo_metodos/celdas.html", context)

@login_required
def metodos(request):
    titulo="Metodos"
    metodos=Metodo.objects.all()
    if request.method == "POST":
        form = MetodoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Método creado satisfactoriamente")
            return redirect("metodos")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = MetodoForm() 
    context={
        "titulo":titulo,
        "form":form,
        "metodos":metodos,
        
    }
    return render(request, "protocolo_metodos/metodos.html", context)

@login_required
def editar_metodos(request, pk):
    titulo="Editar metodos"
    metodos=Metodo.objects.get(id=pk)
    if request.method == "POST":
        form = MetodoForm(request.POST, instance=metodos)
        if form.is_valid():
            form.save()
            messages.success(request, "Método editado satisfactoriamente")
            return redirect("metodos")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = MetodoForm(instance=metodos) 
    context={
        "titulo":titulo,
        "form":form,
        "metodos":metodos,
        
    }
    return render(request, "protocolo_metodos/metodos.html", context)

@login_required
def tipo_muestra(request):
    titulo="Tipo de Muestras"
    tipo_muestra=Tipo_muestra.objects.all()
    if request.method == "POST":
        form = tipo_muestrasForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de muestra creada satisfactoriamente")
            return redirect("tipo_muestra")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = tipo_muestrasForm() 
    context={
        "titulo":titulo,
        "form":form,
        "tipo_muestra":tipo_muestra,
        
    }
    return render(request, "protocolo_metodos/tipo_muestra.html", context)

@login_required
def editar_tipo_muestra(request, pk):
    titulo="Editar Tipo de Muestras"
    tipo_muestra=Tipo_muestra.objects.get(id=pk)
    if request.method == "POST":
        form = tipo_muestrasForm(request.POST, instance=tipo_muestra)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de muestra editada satisfactoriamente")
            return redirect("tipo_muestra")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = tipo_muestrasForm(instance=tipo_muestra) 
    context={
        "titulo":titulo,
        "form":form,
        "tipo_muestra":tipo_muestra,
        
    }
    return render(request, "protocolo_metodos/tipo_muestra.html", context)

@login_required
def etapas(request):
    titulo="Etapas"
    etapas=Etapa.objects.all()
    ensayo=Ensayo.objects.all()
    if request.method == "POST":
        form = EtapaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Etapa creada satisfactoriamente")
            return redirect("etapas")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = EtapaForm() 
    context={
        "titulo":titulo,
        "form":form,
        "etapas":etapas,
        "ensayo":ensayo,
        
    }
    return render(request, "protocolo_metodos/etapas.html", context)

@login_required
def editar_etapas(request, pk):
    titulo="Editar Etapas de Muestras"
    etapas=Etapa.objects.get(id=pk)
    if request.method == "POST":
        form = EtapaForm(request.POST, instance=etapas)
        if form.is_valid():
            form.save()
            messages.success(request, "Etapa editada satisfactoriamente")
            return redirect("etapas")
        else:
             messages.error(request, "Por favor, revisa los datos ingresados")
    else:
        form = EtapaForm(instance=etapas) 
    context={
        "titulo":titulo,
        "form":form,
        "etapas":etapas,
        
    }
    return render(request, "protocolo_metodos/etapas.html", context)


@login_required
def viavilidad_proceso(request):
    titulo="Viavilidad Proceso"
    viavilidad_proceso=ViabilidadProceso.objects.all()
   
    if request.method == "POST":
        form = viavilidad_procesoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("viavilidad_proceso")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = viavilidad_procesoForm() 
    context={
        "titulo":titulo,
        "form":form,
        "viavilidad_proceso":viavilidad_proceso,
       
        
    }
    return render(request, "protocolo_metodos/viavilidad_proceso.html", context)

@login_required
def editar_viavilidad_proceso(request, pk):
    titulo="Editar Viavilidad Proceso"
    viavilidad_proceso=ViabilidadProceso.objects.get(id=pk)
    if request.method == "POST":
        form = viavilidad_procesoForm(request.POST, instance=viavilidad_proceso)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("viavilidad_proceso")
        else:
             messages.error(request, "Por favor, revisa los datos ingresados")
    else:
        form = viavilidad_procesoForm(instance=viavilidad_proceso) 
    context={
        "titulo":titulo,
        "form":form,
        "viavilidad_proceso":viavilidad_proceso,
        
    }
    return render(request, "protocolo_metodos/viavilidad_proceso.html", context)
































    
        


    
