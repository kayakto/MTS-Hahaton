# Generated by Django 5.1.3 on 2024-11-30 09:31

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeePosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('employee_role', models.CharField(choices=[('руководство', 'Руководство'), ('дизайнер', 'Дизайнер'), ('аналитика', 'Аналитика'), ('backend', 'Backend'), ('frontend', 'Frontend'), ('тестирование', 'Тестирование'), ('продажи', 'Продажи'), ('обслуживание', 'Обслуживание'), ('бэк-офис', 'Бэк-офис')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('unit_type', models.CharField(choices=[('functional_unit', 'Functional Unit'), ('division', 'Division')], max_length=50)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='searcher.unit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='searcher.employeeposition')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='searcher.unit')),
            ],
        ),
    ]