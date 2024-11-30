from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .db_parser import parse_excel_and_save_to_db
from .models import Unit, EmployeePosition, Employee
from .serializers import EmployeeInfoSerializer, EmployeeSerializer


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


@api_view(['POST'])
def search_by_filters(request):
    filters = request.data.get('filters', [])

    if not filters:
        return Response({"error": "No filters provided"}, status=400)

    # Начинаем с пустого набора запросов
    unit_queries = Q()
    employee_queries = Q()

    # Разбиваем фильтры на категории
    for filter_ in filters:
        value = filter_.get('value', '').lower()
        type_ = filter_.get('type', '')

        if type_ in ['Функциональный блок', 'Подразделение']:
            unit_queries |= Q(name__icontains=value) & Q(unit_type__icontains=type_)
        elif type_ == 'Должность':
            employee_queries |= Q(position__name__icontains=value)
        elif type_ == 'Роль':
            employee_queries |= Q(position__employee_role__icontains=value)
        elif type_ in ['Имя', 'Фамилия', 'Город', 'Адрес', 'Телефон', 'Почта']:
            field_map = {
                'Имя': 'first_name',
                'Фамилия': 'last_name',
                'Город': 'city',
                'Адрес': 'address',
                'Телефон': 'phone',
                'Почта': 'email'
            }
            employee_queries |= Q(**{f"{field_map[type_]}__icontains": value})

    employee_unit_query = Q()

    if unit_queries.children:
        matching_units = Unit.objects.filter(unit_queries)

        descendant_units = Unit.objects.none()

        for unit in matching_units:
            descendant_units |= unit.get_descendants(include_self=True)

        all_units = descendant_units.distinct('id')

        employee_unit_query |= Q(unit__in=all_units)

        all_units = descendant_units
        for unit in matching_units:
            all_units |= unit.get_ancestors()

    matching_employees = Employee.objects.filter(employee_queries & employee_unit_query)

    if matching_employees.count() == 0:
        return Response([])

    hierarchy = []

    units = Unit.objects.all()
    for unit in units:
        unit_employees = matching_employees.filter(unit=unit)

        if len(unit_employees) == 0:
            continue

        path = [ancestor.name for ancestor in unit.get_ancestors(include_self=True)]

        hierarchy.append({
            "path": path,
            "employees": [EmployeeInfoSerializer(employee).data for employee in unit_employees]
        })

    return Response(hierarchy)


def build_unit_hierarchy(unit, depth):
    """
    Рекурсивно строит иерархию подразделений до указанной глубины.
    :param unit: Текущее подразделение
    :param depth: Текущая глубина рекурсии
    :return: Словарь с данными подразделения и сотрудниками
    """
    if depth < 0:
        return None  # Если глубина отрицательная, не добавляем вложенные подразделения

    return {
        "id": unit.id,
        "name": unit.name,
        "unit_type": unit.unit_type,
        "employees": EmployeeInfoSerializer(unit.employees.all(), many=True).data,
        "children": [
            build_unit_hierarchy(child, depth - 1) for child in unit.children.all()
        ],
        "children_count": unit.children.count()
    }


@api_view(['GET'])
def get_hierarchy(request):
    """
    Возвращает иерархию подразделений с сотрудниками, ограниченную по глубине.
    Принимает параметры:
    - id: ID подразделения для раскрытия (по умолчанию корневые подразделения)
    - depth: Глубина раскрытия иерархии (по умолчанию 2)
    """
    unit_id = request.query_params.get('id')
    depth = int(request.query_params.get('depth', 1))  # По умолчанию глубина 2

    if unit_id:
        # Если указан id, ищем конкретное подразделение
        try:
            unit = Unit.objects.get(id=unit_id)
            hierarchy = build_unit_hierarchy(unit, depth)
        except Unit.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
    else:
        # Если id не указан, возвращаем корневые подразделения
        root_units = Unit.objects.filter(parent__isnull=True)
        hierarchy = [build_unit_hierarchy(unit, depth) for unit in root_units]

    return Response(hierarchy)


def build_branch_hierarchy(unit):
    """
    Рекурсивно строит вложенную иерархию от корня до подразделения сотрудника.
    """
    if unit is None:
        return None

    parent_hierarchy = build_branch_hierarchy(unit.parent)
    current_unit_data = {
        "id": unit.id,
        "name": unit.name,
        "unit_type": unit.unit_type,
    }

    if parent_hierarchy:
        # Вложим текущий узел в children предыдущего уровня
        parent_hierarchy["children"] = [current_unit_data]
        return parent_hierarchy
    else:
        return current_unit_data


@api_view(['GET'])
def get_employee(request, employee_id):
    """
    Возвращает ветку от корневого подразделения до сотрудника.
    :param employee_id: ID сотрудника
    """
    employee = Employee.objects.get(id=employee_id)

    if not employee:
        return Response({"error": "Employee not found"}, status=404)

    return Response(EmployeeSerializer(employee).data)


def get_branch_hierarchy(unit):
    """
    Строит вложенную структуру от корня до указанного подразделения, используя get_ancestors().
    """
    hierarchy = {}
    current_level = hierarchy
    ancestors = unit.get_ancestors(include_self=True)

    for ancestor in ancestors:
        current_level["id"] = ancestor.id
        current_level["name"] = ancestor.name
        current_level["unit_type"] = ancestor.unit_type

        current_level["children"] = {}
        current_level = current_level["children"]

    # Убираем последний пустой контейнер для детей
    current_level.pop("children", None)

    return hierarchy


@api_view(['GET'])
def get_employee_branch(request, employee_id):
    """
    Возвращает ветку от корневого подразделения до сотрудника.
    :param employee_id: ID сотрудника
    """
    employee = Employee.objects.get(id=employee_id)

    if not employee:
        return Response([])

    branch = get_branch_hierarchy(employee.unit)

    return Response(branch)

