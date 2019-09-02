from django.db import models

# Create your models here.

LANDS =(
    (0, "Grunt orny"),
    (1, "Sad"),
    (2, "Łąka trwała"),
    (3, "Pastwisko trwałe"),
)

class AgriculturalLand(models.Model):
    land_name = models.CharField(max_length=256)
    type = models.IntegerField(choices=LANDS)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.TextField(blank=True)

    def __str__(self):
        return self.land_name


class Plants(models.Model):
    plant_name = models.CharField(max_length=256)
    expected_yield = models.DecimalField(max_digits=10, decimal_places=2)
    plant_price = models.DecimalField (max_digits=10, decimal_places=2)
    land_plant = models.ManyToManyField(AgriculturalLand)
    harvest = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sale = models.DecimalField (max_digits=10, decimal_places=2, null=True)
    comments = models.TextField (null=True)

    def __str__(self):
        return self.plant_name

class AgriculturalMachinery(models.Model):
    machinery_name = models.CharField(max_length=256)
    fuel_consumption = models.IntegerField()
    land_machinery = models.ManyToManyField(AgriculturalLand)

    def __str__ (self):
        return self.machinery_name

class ExtraExpenses(models.Model):
    expenses_name = models.CharField(max_length=256)
    cost = models.DecimalField (max_digits=10, decimal_places=2)

    def __str__(self):
        return self.expenses_name

class AdditionalIncome(models.Model):
    income_name = models.CharField(max_length=256)
    cost = models.DecimalField (max_digits=10, decimal_places=2)

    def __str__(self):
        return self.income_name

