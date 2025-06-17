from django.db import models

# Create your models here.
class Consulta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    email = models.EmailField()
    celular = models.CharField(max_length=15)
    tipo_empleo = models.CharField(max_length=1, choices=[('1', 'Relación de dependencia'),('2', 'Independiente')])
    antiguedad_laboral = models.PositiveIntegerField(help_text="En años")
    bruto = models.PositiveIntegerField(help_text="Ingreso bruto mensual")
    propiedad = models.PositiveIntegerField(help_text="Valor de la propiedad")
    ahorros = models.PositiveIntegerField()
    plazo = models.PositiveIntegerField(help_text="Plazo en años")
    
    class Meta:
        db_table = 'consultas'