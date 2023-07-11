# Generated by Django 4.2.3 on 2023-07-09 11:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Bodega',
                'verbose_name_plural': 'Bodegas',
                'db_table': 'Bodega',
            },
        ),
        migrations.CreateModel(
            name='Boleta',
            fields=[
                ('nro_boleta', models.IntegerField(primary_key=True, serialize=False, verbose_name='Nro boleta')),
                ('monto_sin_iva', models.IntegerField(verbose_name='Monto sin IVA')),
                ('iva', models.IntegerField(verbose_name='IVA')),
                ('total_a_pagar', models.IntegerField(verbose_name='Total a pagar')),
                ('fecha_venta', models.DateField(verbose_name='Fecha de venta')),
                ('fecha_despacho', models.DateField(blank=True, null=True, verbose_name='Fecha de despacho')),
                ('fecha_entrega', models.DateField(blank=True, null=True, verbose_name='Fecha de entrega')),
                ('estado', models.CharField(choices=[('Anulado', 'Anulado'), ('Vendido', 'Vendido'), ('Despachado', 'Despachado'), ('Entregado', 'Entregado')], max_length=50, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Boleta',
                'verbose_name_plural': 'Boletas',
                'db_table': 'Boleta',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre categoría')),
            ],
            options={
                'verbose_name': 'Categoría de producto',
                'verbose_name_plural': 'Categorías de productos',
                'db_table': 'Categoria',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre producto')),
                ('descripcion', models.CharField(max_length=400, verbose_name='Descripción')),
                ('precio', models.IntegerField(verbose_name='Precio')),
                ('descuento_subscriptor', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='% Descuento subscriptor')),
                ('descuento_oferta', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='% Descuento oferta')),
                ('imagen', models.ImageField(upload_to='productos/', verbose_name='Imagen')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.categoria', verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'db_table': 'Producto',
                'ordering': ['categoria', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_usuario', models.CharField(choices=[('Cliente', 'Cliente'), ('Administrador', 'Administrador'), ('Superusuario', 'Superusuario')], max_length=50, verbose_name='Tipo de usuario')),
                ('rut', models.CharField(max_length=15, verbose_name='RUT')),
                ('direccion', models.CharField(max_length=400, verbose_name='Dirección')),
                ('subscrito', models.BooleanField(verbose_name='Subscrito')),
                ('imagen', models.ImageField(upload_to='perfiles/', verbose_name='Imagen')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil de usuario',
                'verbose_name_plural': 'Perfiles de usuarios',
                'db_table': 'Perfil',
                'ordering': ['tipo_usuario'],
            },
        ),
        migrations.CreateModel(
            name='DetalleBoleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.IntegerField(verbose_name='Precio')),
                ('descuento_subscriptor', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Descto subs')),
                ('descuento_oferta', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Descto oferta')),
                ('descuento_total', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Descto total')),
                ('descuentos', models.IntegerField(verbose_name='Descuentos')),
                ('precio_a_pagar', models.IntegerField(verbose_name='Precio a pagar')),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.bodega')),
                ('boleta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.boleta')),
            ],
            options={
                'verbose_name': 'Detalle de boleta',
                'verbose_name_plural': 'Detalles de boletas',
                'db_table': 'DetalleBoleta',
            },
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.IntegerField(verbose_name='Precio')),
                ('descuento_subscriptor', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Descto subs')),
                ('descuento_oferta', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Descto oferta')),
                ('descuento_total', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Descto total')),
                ('descuentos', models.IntegerField(verbose_name='Descuentos')),
                ('precio_a_pagar', models.IntegerField(verbose_name='Precio a pagar')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.perfil')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.producto')),
            ],
            options={
                'verbose_name': 'Carrito de compras',
                'verbose_name_plural': 'Carritos de compras',
                'db_table': 'Carrito',
                'ordering': ['cliente', 'producto'],
            },
        ),
        migrations.AddField(
            model_name='boleta',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.perfil'),
        ),
        migrations.AddField(
            model_name='bodega',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.producto', verbose_name='Producto'),
        ),
    ]
