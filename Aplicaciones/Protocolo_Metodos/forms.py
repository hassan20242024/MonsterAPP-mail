from django import forms
from django.contrib import admin
from django.forms.widgets import NumberInput
from django.contrib.admin.widgets import AutocompleteSelect
from django_select2 import forms as s2forms


#from simple_autocomplete.widgets import AutoCompleteWidget


from .models import Protocolos, Parametro, Metodologia, EstadoProtocolo,Ensayo,Viabilidad, Subparametro,Titulo_Parametro, Muestras_y_Placebos, Cliente, Celda, Metodo, Tipo_muestra, Etapa
from Aplicaciones.Secuencias.models import Sistema
from Aplicaciones.Protocolo_Muestras.models import ViabilidadProceso

class ProtocolosForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.Textarea(attrs={'rows':6, 'placeholder': 'Título del Protocolo'}))
    

    fecha_ingreso=forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    #fecha_final=forms.DateField(widget=NumberInput( attrs={'type': 'date'}))

    Insumos_del_Proceso = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,queryset=Viabilidad.objects.all()
        )
    
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'rows':6}))

    class Meta:
        model=Protocolos
        fields = '__all__'
        exclude=["condicion"]
        



class ParametroForm(forms.ModelForm):
    class Meta:
        order_by=('tittle')
        fields = '__all__'
        model=Parametro
        exclude=["condicion"]

class SubparametroForm(forms.ModelForm):
    class Meta:
        model=Subparametro
        fields = '__all__'
        exclude=["condicion"] 

class Titulo_ParametroForm(forms.ModelForm):
    class Meta:
        model=Titulo_Parametro
        exclude=["condicion"]         

class MetodologiaForm(forms.ModelForm):
    class Meta:
        model=Metodologia
        exclude=["condicion"]

class EstadoProtocoloForm(forms.ModelForm):
    class Meta:
        model=EstadoProtocolo
        exclude=["condicion"]  

class crear_ensayoForm(forms.ModelForm):
    class Meta:
        model=Ensayo
        exclude=["condicion"] 

class ViabilidadForm(forms.ModelForm):
    class Meta:
        model=Viabilidad
        exclude=["condicion"] 

class ingresar_muestrasForm(forms.ModelForm):
    fecha_ingreso=forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    observaciones_muestras = forms.CharField(widget=forms.Textarea(attrs={'rows':4}))
    class Meta:
        fields = '__all__'
        model=Muestras_y_Placebos
        exclude=["condicion"]                     

class clienteForm(forms.ModelForm):
    class Meta:
        model=Cliente
        exclude=["condicion"] 

class sistemaForm(forms.ModelForm):
    class Meta:
        model=Sistema
        exclude=["condicion"] 

class CeldaForm(forms.ModelForm):
    class Meta:
        model=Celda
        exclude=["condicion"] 
        
class MetodoForm(forms.ModelForm):
    class Meta:
        model=Metodo
        exclude=["condicion"]  

class tipo_muestrasForm(forms.ModelForm):
    class Meta:
        model=Tipo_muestra
        exclude=["condicion"]  

class EtapaForm(forms.ModelForm):
    class Meta:
        model=Etapa
        exclude=["condicion"] 


class viavilidad_procesoForm(forms.ModelForm):
    class Meta:
        model=ViabilidadProceso
        exclude=["condicion"]                                     



                 




         


  
        

   
        

   