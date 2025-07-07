from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0, message="El precio no puede ser menor a 0.")])
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre