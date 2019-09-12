# Generated by Django 2.2.4 on 2019-09-05 22:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AgriculturalLand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('land_name', models.CharField(max_length=256)),
                ('type', models.IntegerField(choices=[(0, 'Grunt orny'), (1, 'Sad'), (2, 'Łąka trwała'), (3, 'Pastwisko trwałe')])),
                ('area', models.DecimalField(decimal_places=2, max_digits=10)),
                ('comments', models.TextField(blank=True)),
                ('user_log', models.ForeignKey(on_delete='models.CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_name', models.CharField(max_length=256)),
                ('expected_yield', models.DecimalField(decimal_places=2, max_digits=10)),
                ('plant_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('harvest', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('sale', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('comments', models.TextField(blank=True)),
                ('time_add', models.DateField()),
                ('land_plant', models.ManyToManyField(to='farmlife.AgriculturalLand')),
                ('user_log', models.ForeignKey(on_delete='models.CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExtraExpenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expenses_name', models.CharField(max_length=256)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time_add', models.DateField()),
                ('user_log', models.ForeignKey(on_delete='models.CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AgriculturalMachinery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machinery_name', models.CharField(max_length=256)),
                ('fuel_consumption', models.IntegerField()),
                ('accessories', models.CharField(blank=True, max_length=256)),
                ('accessories_width', models.IntegerField(blank=True)),
                ('time_add', models.DateField()),
                ('land_machinery', models.ManyToManyField(blank=True, to='farmlife.AgriculturalLand')),
                ('user_log', models.ForeignKey(on_delete='models.CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalIncome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_name', models.CharField(max_length=256)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time_add', models.DateField()),
                ('user_log', models.ForeignKey(on_delete='models.CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
