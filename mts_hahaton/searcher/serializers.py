from rest_framework import serializers
from .models import Unit, EmployeePosition, Employee


class UnitSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('name', 'type')

    def get_type(self, obj):
        return "Подразделение"


class EmployeePositionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = EmployeePosition
        fields = ('name', 'type')

    def get_type(self, obj):
        return "Должность"


class EmployeeRoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="employee_role")
    type = serializers.SerializerMethodField()

    class Meta:
        model = EmployeePosition
        fields = ('name', 'type')

    def get_type(self, obj):
        return "Роль"


class EmployeeSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('name', 'type')

    def get_type(self, obj):
        return "Сотрудник"
