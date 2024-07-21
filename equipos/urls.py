from django.urls import path, include
from equipos.views import *

from django.contrib.auth.views import LogoutView,LoginView


urlpatterns = [
    
    path('', home, name ="home"), 

    #____ Usuarios
    path('usuario/', UsuarioList.as_view(), name="usuario"),    
    path('usuarioCreate/', UsuarioCreate.as_view(), name="usuarioCreate"), 
    path('usuarioUpdate/<int:pk>/', UsuarioUpdate.as_view(), name="usuarioUpdate"), 
    path('usuarioDelete/<int:pk>/', UsuarioDelete.as_view(), name="usuarioDelete"), 


    #____ Observación
    path('observacion/', observaciones, name ="observacion"), 

    #____ Un poco de información sobre mí
    path('acerca/', acerca, name="acerca"),

    #____ Equipos
    path('equipo/', equipos, name ="equipo"), 
    path('equiposUpdate/<equipo_equipo>/', equiposUpdate, name ="equiposUpdate"), 
    path('equiposDelete/<equipo_equipo>/', equiposDelete, name ="equiposDelete"), 
        
    #Formularios:
    path('equipo/', EquipoForm, name ="equipo"),
    path('usuario/', UsuarioForm, name ="usuario"),
    path('observacion/', ObservacionForm, name ="observacion"),     

    #_____ Login / Logout / Registration
    path('login/', loginRequest, name="login"), 
    path('logout/', LogoutView.as_view(template_name="equipos/logout.html"), name="logout"),
    path('registro/', registro, name="registro"), 

    #_____ Editar perfil / Avatar
    path('perfil/', editPerfil, name="perfil"), 
    path('<int:pk>/password/', CambiarClave.as_view(), name="cambiarClave"),    
    path('agregar_avatar/', agregarAvatar, name="agregar_avatar"), 

]

    