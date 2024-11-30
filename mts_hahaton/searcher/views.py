from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .db_parser import parse_excel_and_save_to_db
from .models import Unit, EmployeePosition, Employee


@api_view(['GET'])
def import_excel(request):
    parse_excel_and_save_to_db('searcher/file.xlsx')
    return Response("OK")


@api_view(['GET'])
def search_filters(request, search_text):
    query = search_text.lower()

    units = Unit.objects.filter(name__icontains=query)
    positions = EmployeePosition.objects.filter(name__icontains=query)
    roles = EmployeePosition.objects.filter(employee_role__icontains=query)
    employees = Employee.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(city__icontains=query) |
        Q(phone__icontains=query) |
        Q(address__icontains=query) |
        Q(email__icontains=query)
    )

    units_data = set()
    for unit in units:
        if query.lower() in unit.name.lower():
            units_data.add((unit.name, unit.unit_type))

    positions_data = set()
    for position in positions:
        if query.lower() in position.name.lower():
            positions_data.add((position.name, "Должность"))

    roles_data = set()
    for role in roles:
        if query.lower() in role.employee_role.lower():
            roles_data.add((role.employee_role, "Роль"))

    employees_data = set()
    for employee in employees:
        matches = {}
        if query.lower() in employee.first_name.lower():
            matches['Имя'] = employee.first_name
        if query.lower() in employee.last_name.lower():
            matches['Фамилия'] = employee.last_name
        if employee.city and query.lower() in employee.city.lower():
            matches['Город'] = employee.city
        if employee.address and query.lower() in employee.address.lower():
            matches['Адрес'] = employee.address
        if employee.phone and query.lower() in employee.phone.lower():
            matches['Телефон'] = employee.phone
        if employee.email and query.lower() in employee.email.lower():
            matches['Почта'] = employee.email
        for field, value in matches.items():
            employees_data.add((value, field))

    results = ([{"value": value, "type": type_} for value, type_ in units_data] +
               [{"value": value, "type": type_} for value, type_ in positions_data] +
               [{"value": value, "type": type_} for value, type_ in roles_data] +
               [{"value": value, "type": type_} for value, type_ in employees_data])

    return Response(results)
