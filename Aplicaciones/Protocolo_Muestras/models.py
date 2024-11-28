from django.db import models
from Aplicaciones.Protocolo_Metodos.models import Ensayo,Metodologia, Celda, Cliente, Muestras_y_Placebos, EstadoProtocolo, Metodo
import datetime


# Create your models here.

#3class Estado_Proceso(models.Model):
   
  #  estado_proceso=models.CharField(verbose_name="Estado del proceso", max_length=90)
   # estado_motivo=models.CharField(verbose_name="Motivo del estado", max_length=90, blank=True, null=False, unique=True)
    #class Condicion(models.TextChoices):
     #   ACTIVO = "Activo", "ACTIVO"
      #  PASIVO = "Pasivo", "PASIVO"
    #condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")
    #def estado_protocolo_proceso(self):
     #   return "{} {}".format(self.estado_proceso, self.estado_motivo)    
   
   # def __str__(self):    

    #    return str(self.estado_protocolo_proceso()) 

class ViabilidadProceso(models.Model):
   
    nombre_viabilidad=models.CharField(verbose_name="Insumos del Proceso", max_length=90, null=True, blank=False, unique=True)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
   
    def __str__(self):    

        return(self.nombre_viabilidad)
    
class Proceso(models.Model):
     fecha_ingreso=models.DateField(verbose_name="Fecha de Registro", null=True, blank=False, help_text=u"AAAA/MM/DD")
     codigo=models.CharField(max_length=90, verbose_name="Código Protocolo", null=True, blank=False, unique=True)
     nombre=models.CharField(max_length=250, verbose_name="Título_del_Protocolo",  null=True, blank=False, unique=True)
     ensayos=models.ManyToManyField(to=Ensayo, blank=False)
     celda=models.ForeignKey(to=Celda, on_delete=models.CASCADE, verbose_name="Celda", null=True, blank=False)
     muestras=models.ManyToManyField(Muestras_y_Placebos, blank=False)
     metodologia=models.ForeignKey(Metodologia, on_delete=models.CASCADE, verbose_name="metodologia", null=True, blank=False,  max_length=90)
     #parametro=models.ManyToManyField(to=Parametro, blank=False, related_name="parametro")
     Insumos_del_Proceso=models.ManyToManyField(to=ViabilidadProceso)
     cliente=models.ForeignKey(to=Cliente, on_delete=models.CASCADE, verbose_name="Cliente", null=True, blank=False)
     metodo=models.ForeignKey(to=Metodo, on_delete=models.CASCADE, verbose_name="Metodo de referencia", null=True, blank=False)
     estado_del_proceso=models.ForeignKey(to=EstadoProtocolo, on_delete=models.CASCADE, verbose_name="Estado del proceso", null=True, blank=False)
     class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
     condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
     observaciones=models.CharField(max_length=250, verbose_name="Observaciones",  null=True, blank=False)
     fecha_final=models.DateField(verbose_name="Fecha de Finalización", null=True, blank=True,default=datetime.datetime.now)

     def __str__(self):        
        return str(self.codigo)
    
