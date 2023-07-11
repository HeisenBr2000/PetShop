from django import forms
from django.forms import ModelForm, fields, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Categoria, Producto, Bodega, Perfil


form_hidden = {'class': 'd-none'}
form_select = {'class': 'form-select'}
form_control = {'class': 'form-control'}
form_text_area = {'class': 'form-control', 'rows': '3'}
form_file = {'class': 'form-control-file', 'title': 'Debe subir una imagen'}
form_check = {'class': 'form-check-input'}
form_password = {'class': 'form-control text-danger', 'value': '123'}

class ProductoForm(forms.ModelForm):
    eliminar = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    class Meta:
        model = Producto
        fields = '__all__'

        widgets = {
            'categoria': forms.Select(attrs=form_select),
            'nombre': forms.TextInput(attrs=form_control),
            'descripcion': forms.Textarea(attrs=form_text_area),
            'precio': forms.NumberInput(attrs=form_control),
            'descuento_subscriptor': forms.NumberInput(attrs=form_control),
            'descuento_oferta': forms.NumberInput(attrs=form_control),
            'imagen': forms.FileInput(attrs=form_file),
        }




class BodegaForm(forms.Form):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs=form_select),
        label='Categoría'
    )
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.Select(attrs=form_select),
        label='Producto'
    )
    cantidad = forms.IntegerField(
        widget=forms.NumberInput(attrs=form_control),
        label='Cantidad'
    )
    
    def __init__(self, *args, **kwargs):
        super(BodegaForm, self).__init__(*args, **kwargs)
        
        if 'categoria' in self.data:
            categoria_id = self.data.get('categoria')
            self.fields['producto'].queryset = Producto.objects.filter(categoria_id=categoria_id)
    
    class Meta:
        fields = '__all__'


class RegistroClienteForm(UserCreationForm):

    rut = forms.CharField(
        max_length=15, 
        required=True, 
        label='RUT',
        widget=forms.TextInput(attrs=form_control),
    )
    direccion = forms.CharField(
        max_length=400, 
        required=True, 
        label='Dirección',
        widget=forms.Textarea(attrs=form_text_area),
    )
    subscrito = forms.BooleanField(
        required=False,
        label='Subscrito',
        widget=forms.CheckboxInput(attrs=form_check),
    )
    imagen = forms.CharField(
        required=True,
        label='Imagen',
        widget=forms.FileInput(attrs=form_file),
    )
    
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'rut', 
            'direccion', 
            'subscrito', 
            'imagen', 
            'password1', 
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(form_control)
        self.fields['first_name'].widget.attrs.update(form_control)
        self.fields['last_name'].widget.attrs.update(form_control)
        self.fields['email'].widget.attrs.update(form_control)
        self.fields['password1'].widget.attrs.update(form_control)
        self.fields['password2'].widget.attrs.update(form_control)


class IngresarForm(Form):
    username = forms.CharField(widget=forms.TextInput(attrs=form_control), label="Cuenta")
    password = forms.CharField(widget=forms.PasswordInput(attrs=form_control), label="Contraseña")
    class Meta:
        fields = ['username', 'password']



class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = '__all__'

        widgets = {
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'subscrito': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
        } 

      