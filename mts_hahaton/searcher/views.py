import os.path

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Unit, EmployeePosition, Employee
from .serializers import UnitSerializer, EmployeePositionSerializer, EmployeeSerializer, \
    EmployeeRoleSerializer
from .db_parser import parse_excel_and_save_to_db


@api_view(['GET'])
def import_excel(request):
    parse_excel_and_save_to_db('searcher/file.xlsx')
    return Response("Hello world!")


@api_view(['GET'])
def search_filters(request, search_text: str):
    query = search_text.lower()

    units = Unit.objects.filter(name__icontains=query)
    positions = EmployeePosition.objects.filter(name__icontains=query)
    roles = EmployeePosition.objects.filter(employee_role__icontains=query)
    employees = Employee.objects.filter(
        Q(name__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    )

    units_data = UnitSerializer(units, many=True).data
    positions_data = EmployeePositionSerializer(positions, many=True).data
    roles_data = EmployeeRoleSerializer(roles, many=True).data
    employees_data = EmployeeSerializer(employees, many=True).data

    results = units_data + positions_data + roles_data + employees_data

    return Response(results)
