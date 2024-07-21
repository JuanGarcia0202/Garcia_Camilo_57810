from django.shortcuts import render, redirect
from django.urls import reverse_lazy

#Modelos:
from equipos.models import *

#Formularios:
from equipos.forms import *

from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.views import PasswordChangeView 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "equipos/index.html") 

def acerca(request):
    return render(request, "equipos/acerca.html")

#____Equipos
@login_required
def equipos(request):
    search_form = EquipoSearchForm(request.GET or None)
    search_term = ''

    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']

    if request.method == "POST":
        equipoForm = EquipoForm(request.POST)
        if equipoForm.is_valid():
            equipoForm.save()
            return redirect('equipo')
    else:
        equipoForm = EquipoForm()

    equipos = Equipo.objects.filter(equipo__icontains=search_term) if search_term else Equipo.objects.all()

    contexto = {
        "equipoForm": equipoForm,
        "equipos": equipos,
        "search_form": search_form,
    }
    return render(request, "equipos/equipo.html", contexto)

@login_required
def equiposUpdate(request, equipo_equipo):
    equipos = Equipo.objects.get(equipo=equipo_equipo)
    if request.method == "POST":
        equipoForm = EquipoForm(request.POST)
        if equipoForm.is_valid():
            equipos.equipo = equipoForm.cleaned_data.get("equipo")
            equipos.marca = equipoForm.cleaned_data.get("marca")
            equipos.modelo = equipoForm.cleaned_data.get("modelo")
            equipos.serie = equipoForm.cleaned_data.get("serie")
            equipos.placa = equipoForm.cleaned_data.get("placa")
            equipos.save()
            contexto = {"equipo": Equipo.objects.all() }
            return render(request, "equipos/equipo.html", contexto) 
    else:
        equipoForm =  EquipoForm(initial={"equipo": equipos.equipo, 
                                          "marca": equipos.marca, 
                                          "modelo": equipos.modelo, 
                                          "serie": equipos.serie, 
                                          "placa": equipos.placa})
    
    return render(request, "equipos/equipo.html", {"form": equipoForm})

@login_required
def equiposDelete(request, equipo_equipo):
    equipos = Equipo.objects.get(equipo=equipo_equipo)
    equipos.delete()
    contexto = {"equipo": Equipo.objects.all() }
    return render(request, "equipos/equipo.html", contexto) 


#____Usuarios
class UsuarioList(LoginRequiredMixin, ListView):
    model = Usuario

class UsuarioCreate(LoginRequiredMixin, CreateView):
    model = Usuario
    fields = ["nombre", "ubicacion"]
    success_url = reverse_lazy("usuario")

class UsuarioUpdate(LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ["nombre", "ubicacion"]
    success_url = reverse_lazy("usuario")

class UsuarioDelete(LoginRequiredMixin, DeleteView):
    model = Usuario
    success_url = reverse_lazy("usuario")


#____Observaciones
@login_required
def observaciones(request):
    search_form = ObservacionSearchForm(request.GET or None)
    search_term = ''

    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']

    if request.method == "POST":
        observacionForm = ObservacionForm(request.POST)
        if observacionForm.is_valid():
            observacionForm.save()
            return redirect('observacion')
    else:
        observacionForm = ObservacionForm()

    observaciones = Observacion.objects.filter(observacion__icontains=search_term) if search_term else Observacion.objects.all()

    contexto = {
        "observacionForm": observacionForm,
        "observaciones": observaciones,
        "search_form": search_form,
    }
    return render(request, "equipos/observacion.html", contexto)

#______ Login / Logout / Registration

def loginRequest(request):
    if request.method == "POST":
        usuario = request.POST["username"]
        clave = request.POST["password"]
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)

            #_______ Buscar el avatar
            try:
                avatar = Avatar.objects.get(user=request.user.id).imagen.url
            except:
                avatar = "/media/avatares/default.png"
            finally:
                request.session["avatar"] = avatar 
            return render(request, "equipos/index.html")
        else:
            return redirect(reverse_lazy('login'))

    else:
        miForm = AuthenticationForm()

    return render(request, "equipos/login.html", {"form": miForm})


def registro(request):
    if request.method == "POST":
        miForm = RegistroForm(request.POST)
        if miForm.is_valid():
            usuario = miForm.cleaned_data.get("username")
            miForm.save()
            return redirect(reverse_lazy('home'))

    else:
        miForm = RegistroForm()

    return render(request, "equipos/registro.html", {"form": miForm})

@login_required
def editPerfil(request):
    usuario = request.user
    if request.method == "POST":
        miForm = UserEditForm(request.POST)
        if miForm.is_valid():
            user = User.objects.get(username=usuario)
            user.email = miForm.cleaned_data.get("email")
            user.first_name = miForm.cleaned_data.get("fist_name")
            user.last_name = miForm.cleaned_data.get("last_name")
            user.save()
            return redirect(reverse_lazy("home"))
    else:
        miForm = UserEditForm(instance=usuario)
    return render(request, "equipos/editarPerfil.html", {"form": miForm})

class CambiarClave(LoginRequiredMixin, PasswordChangeView):
    template_name = "equipos/cambiarClave.html"
    success_url = reverse_lazy("home")

@login_required
def agregarAvatar(request):
    usuario = request.user
    if request.method == "POST":
        miForm = AvatarForm(request.POST, request.FILES)
        if miForm.is_valid():
            usuario = User.objects.get(username=request.user)
            imagen = miForm.cleaned_data["imagen"]
            # Para borrar avatares antiguos
            avatarViejo = Avatar.objects.filter(user=usuario)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()
            #_________________
            avatar = Avatar(user=usuario, imagen=imagen)
            avatar.save()

            #________________
            imagen = Avatar.objects.get(user=usuario).imagen.url
            request.session["avatar"] = imagen 


            return redirect(reverse_lazy("home"))
    else:
        miForm = UserEditForm(instance=usuario)
    return render(request, "equipos/agregarAvatar.html", {"form": miForm})

