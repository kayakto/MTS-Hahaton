from rest_framework import serializers
from .models import Unit, EmployeePosition, Employee


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name', 'parent', 'unit_type']


class EmployeePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePosition
        fields = ['id', 'name', 'employee_role']


class EmployeeSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)
    position = EmployeePositionSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'unit',
            'position',
            'first_name',
            'last_name',
            'phone',
            'city',
            'address',
            'email'
        ]


class EmployeeInfoSerializer(serializers.ModelSerializer):
    position = EmployeePositionSerializer(read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id',
            'position',
            'name',
            'phone',
            'city',
            'address',
            'email'
        ]

    def get_name(self, obj):
        """Возвращает объединенное имя"""
        return f"{obj.last_name} {obj.first_name}"


# Если нужна возможность обновлять или создавать объект Employee, можно добавить методы:
class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'unit',
            'position',
            'first_name',
            'last_name',
            'phone',
            'city',
            'address',
            'email'
        ]