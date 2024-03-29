# Generated by Django 3.2.1 on 2021-05-17 18:02

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('address', models.TextField(max_length=1000, verbose_name='Address')),
                ('phone', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.PositiveIntegerField(default=0, verbose_name='Cost')),
            ],
            options={
                'verbose_name': 'Composition',
                'verbose_name_plural': 'Compositions',
            },
        ),
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('type', models.CharField(choices=[('dessert', 'Dessert'), ('drink', 'Drink'), ('other', 'Other')], default='other', max_length=20, verbose_name='Type')),
                ('price', models.PositiveIntegerField(verbose_name='Price')),
                ('discount_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Discount Price')),
            ],
            options={
                'verbose_name': 'Extra',
                'verbose_name_plural': 'Extras',
                'ordering': ('name', 'type'),
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('audio_file_name', models.CharField(blank=True, max_length=255, verbose_name='Music')),
                ('available', models.BooleanField(default=True, verbose_name='Available')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Image')),
                ('font_name', models.CharField(blank=True, max_length=255, verbose_name='Font')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Price')),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menus',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('number', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('preparing', 'Preparing'), ('ready', 'Ready'), ('on_delivery', 'On Delivery'), ('delivered', 'Delivered'), ('canceled', 'Canceled'), ('no_answer', 'No Answer'), ('ditched', 'Ditched')], default='pending', max_length=20)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='mainapp.client', verbose_name='Client')),
            ],
        ),
        migrations.CreateModel(
            name='ZeUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('phone', models.CharField(max_length=255, unique=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_deliveryman', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('position', models.PositiveIntegerField(default=1, verbose_name='Position')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.menu', verbose_name='Menu')),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=255, unique=True, verbose_name='Phone Number')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='mainapp.client', verbose_name='Client')),
            ],
            options={
                'verbose_name': 'Phone Number',
                'verbose_name_plural': 'Phone Numbers',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('composition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.composition', verbose_name='Composition')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='mainapp.order', verbose_name='Order')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Price')),
                ('discount_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Discount Price')),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Image')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.section', verbose_name='Section')),
            ],
            options={
                'verbose_name': 'Food',
                'verbose_name_plural': 'Foods',
                'ordering': ('name', 'section__position'),
            },
        ),
        migrations.CreateModel(
            name='CompositionFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_price', models.PositiveIntegerField(default=0, verbose_name='Food Price')),
                ('composition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.composition', verbose_name='Composition')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.food', verbose_name='Food')),
            ],
            options={
                'ordering': ('food__section__position',),
            },
        ),
        migrations.AddField(
            model_name='composition',
            name='extras',
            field=models.ManyToManyField(related_name='compositions', to='mainapp.Extra', verbose_name='Extras'),
        ),
        migrations.AddField(
            model_name='composition',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.menu', verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='composition',
            name='selected_foods',
            field=models.ManyToManyField(through='mainapp.CompositionFood', to='mainapp.Food', verbose_name='Selected Foods'),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(max_length=1000, verbose_name='Address')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='mainapp.client', verbose_name='Client')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
                'ordering': ('id',),
            },
        ),
    ]
