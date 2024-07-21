from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=60)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre}, {self.ubicacion}"

class Equipo(models.Model):
    equipo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    serie = models.CharField(max_length=50)
    placa = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.equipo}, {self.marca}, {self.modelo}, {self.serie}, {self.placa}"   

class Observacion(models.Model):
    observacion = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.observacion}"
    
class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatares")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user}{self.imagen}"
