from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Unit(MPTTModel):
    name = models.CharField(max_length=255, db_collation="nocase")
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
    unit_type = models.CharField(
        max_length=50,
        choices=[('функциональный блок', 'Функциональный блок'), ('подразделение', 'Подразделение')]
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class EmployeePosition(models.Model):
    name = models.CharField(max_length=100)
    employee_role = models.CharField(
        max_length=50,
        choices=[("руководство", "Руководство"),
                 ("дизайнер", "Дизайнер"),
                 ("аналитика", "Аналитика"),
                 ("backend", "Backend"),
                 ("frontend", "Frontend"),
                 ("тестирование", "Тестирование"),
                 ("продажи", "Продажи"),
                 ("обслуживание", "Обслуживание"),
                 ("бэк-офис", "Бэк-офис")]
    )


class Employee(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='employees')
    position = models.ForeignKey(EmployeePosition, on_delete=models.CASCADE, related_name='employees')
    first_name = models.CharField(max_length=100, db_collation="nocase")
    last_name = models.CharField(max_length=100, db_collation="nocase")
    phone = models.CharField(max_length=100, null=True, db_collation="nocase")
    city = models.CharField(max_length=255, null=True, db_collation="nocase")
    address = models.CharField(max_length=100, null=True, db_collation="nocase")
    email = models.CharField(max_length=100, null=True, db_collation="nocase")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
