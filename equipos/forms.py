from django import forms
from equipos.models import Equipo, Usuario, Observacion
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['equipo','marca', 'modelo', 'serie', 'placa']

class EquipoSearchForm(forms.Form):
    search_term = forms.CharField(max_length=100, required=False, label='Buscar Equipo')

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'ubicacion']

class UsuarioSearchForm(forms.Form):
    search_term = forms.CharField(max_length=100, required=False, label='Buscar Usuario')
    
class ObservacionForm(forms.ModelForm):
    class Meta:
        model = Observacion
        fields = ['observacion']

class ObservacionSearchForm(forms.Form):
    search_term = forms.CharField(max_length=100, required=False, label='Buscar Observacion')

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Contraseña a confirmar", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserEditForm(UserChangeForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="Nombre", max_length=50, required=True)
    last_name = forms.CharField(label="Apellido", max_length=50, required=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

class AvatarForm(forms.Form):
    imagen = forms.ImageField(required=True)