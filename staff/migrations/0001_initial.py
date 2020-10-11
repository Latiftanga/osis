# Generated by Django 3.1.1 on 2020-10-10 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import staff.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveIntegerField(choices=[(1, 'Teaching'), (2, 'Non Teaching')])),
                ('job_title', models.CharField(max_length=64)),
                ('job_description', models.CharField(blank=True, max_length=255)),
                ('date_employed', models.DateField()),
                ('staff_id', models.CharField(blank=True, max_length=16)),
                ('registered_no', models.CharField(blank=True, max_length=16)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, choices=[('Mr', 'Mr'), ('Ms', 'Ms'), ('Mrs', 'Mrs'), ('Dr', 'Dr'), ('Prof', 'Prof'), ('Rev', 'Rev'), ('Maulvi', 'Maulvi')], max_length=32)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('middle_name', models.CharField(blank=True, max_length=32)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('sssnit_no', models.CharField(blank=True, max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
                ('image', models.ImageField(blank=True, null=True, upload_to=staff.models.staff_image_file_path)),
                ('account', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL)),
                ('appointment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='staff.appointment')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='core.school')),
            ],
            options={
                'verbose_name': 'staff',
                'verbose_name_plural': 'staff',
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_promoted', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.grade')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promotions', to='staff.staff')),
            ],
            options={
                'ordering': ['-date_promoted'],
            },
        ),
        migrations.AddField(
            model_name='grade',
            name='promotions',
            field=models.ManyToManyField(through='staff.Promotion', to='staff.Staff'),
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Academic', 'Academic'), ('Professional', 'Professional'), ('Hybrid', 'Hybrid')], max_length=16)),
                ('title', models.CharField(max_length=255)),
                ('certificate_date', models.DateField()),
                ('certificate_code', models.CharField(blank=True, max_length=8)),
                ('certificate_description', models.CharField(blank=True, max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=64)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='staff.staff')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to='staff.grade'),
        ),
    ]
