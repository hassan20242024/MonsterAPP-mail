from django import forms
from django.contrib import admin
from django.forms.widgets import NumberInput
from django.contrib.admin.widgets import AutocompleteSelect
from django_select2 import forms as s2forms
from .models import Protocolos,Sistema,Parametro,Lavado_buzo
from django.core.exceptions import ValidationError
from django.core import validators




#from simple_autocomplete.widgets import AutoCompleteWidget


from .models import Secuencias

class secuenciasForm(forms.ModelForm):
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'rows':5}), required=True)
    #invalidez = forms.ModelChoiceField(
    #empty_label= ("Seleccione el motivo"),
    #queryset=Invalidar_Secuencia.objects.all(),
    #required=False)
    #fecha_Inicio = forms.DateField(widget=forms.DateInput(format='%d.%B.%Y'),
        #input_formats=['%d.%B.%Y']
    #)
    #fecha_Inicio = forms.DateTimeField(
        #label="Fecha de Inicio",
        #required=True,
       # widget=forms.DateTimeInput(format=["%Y-%m-%d %H:%M:%S"], attrs={"type": "datetime-local"}),
        #input_formats=["%Y-%m-%d %H:%M:%S"]
    #)
    
   
    class Meta:
        model=Secuencias
        fields = '__all__'
        #exclude=["condicion"] 

    #def clean_observaciones(self):
        #cleaned_data = super(secuenciasForm, self).clean()
        #observaciones=cleaned_data.get("Observaciones")
      
        #if observaciones[0].lower() != 'd':
        
        
            #raise forms.ValidationError("PILAS")
        #return observaciones   
class buzosForm(forms.ModelForm):
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'rows':8}), required=True)
    class Meta:
        model= Lavado_buzo
        fields = '__all__'
        exclude = ["condicion"]


