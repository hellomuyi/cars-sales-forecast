# Generated by Django 2.2.17 on 2021-01-09 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_date', models.CharField(blank=True, max_length=255, null=True)),
                ('car_class', models.CharField(blank=True, max_length=255, null=True)),
                ('sale_qut', models.CharField(blank=True, max_length=255, null=True)),
                ('compartment', models.CharField(blank=True, max_length=255, null=True)),
                ('tr', models.CharField(blank=True, db_column='TR', max_length=255, null=True)),
                ('gearbox_type', models.CharField(blank=True, max_length=255, null=True)),
                ('displacement', models.CharField(blank=True, max_length=255, null=True)),
                ('charge', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.CharField(blank=True, max_length=255, null=True)),
                ('driven_type', models.CharField(blank=True, max_length=255, null=True)),
                ('fuel_type', models.CharField(blank=True, max_length=255, null=True)),
                ('newenergy', models.CharField(blank=True, max_length=255, null=True)),
                ('emission', models.CharField(blank=True, max_length=255, null=True)),
                ('mvp', models.CharField(blank=True, max_length=255, null=True)),
                ('luxurious', models.CharField(blank=True, max_length=255, null=True)),
                ('power', models.CharField(blank=True, max_length=255, null=True)),
                ('cylinder', models.CharField(blank=True, max_length=255, null=True)),
                ('engine', models.CharField(blank=True, max_length=255, null=True)),
                ('car_len', models.CharField(blank=True, max_length=255, null=True)),
                ('car_width', models.CharField(blank=True, max_length=255, null=True)),
                ('car_height', models.CharField(blank=True, max_length=255, null=True)),
                ('total_quality', models.CharField(blank=True, max_length=255, null=True)),
                ('equipment_quality', models.CharField(blank=True, max_length=255, null=True)),
                ('rated_passenger', models.CharField(blank=True, max_length=255, null=True)),
                ('wheelbase', models.CharField(blank=True, max_length=255, null=True)),
                ('front_track', models.CharField(blank=True, max_length=255, null=True)),
                ('rear_track', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Carname',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_name', models.CharField(blank=True, max_length=255, null=True)),
                ('class_id', models.CharField(blank=True, max_length=255, null=True)),
                ('car_url', models.ImageField(upload_to='car/')),
            ],
        ),
        migrations.CreateModel(
            name='Username',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=45, unique=True)),
                ('user_password', models.CharField(max_length=45)),
                ('user_photo', models.ImageField(upload_to='')),
            ],
        ),
    ]
