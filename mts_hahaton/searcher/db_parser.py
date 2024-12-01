import openpyxl
from django.core.management import call_command
from django.db import transaction
from .models import *


def parse_excel_and_save_to_db(file_path):
    call_command('migrate')

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    if Unit.objects.count() > 0:
        print("Db is already parsed")
        return

    with transaction.atomic():
        for row in sheet.iter_rows(min_row=2, values_only=True):
            unit_1_name = row[0]
            functional_block = row[1]
            unit_2_name = row[2]
            unit_3_name = row[3]
            unit_4_name = row[4]
            position_name = row[5]
            role = row[6]
            last_name = row[7]
            first_name = row[8]
            phone = row[9]
            city = row[10]
            address = row[11]
            email = row[12]

            if not unit_1_name:
                continue

            unit_1 = Unit.objects.get_or_create(
                name=str.strip(unit_1_name),
                parent=None,
                unit_type='подразделение'
            )[0]

            unit_2 = unit_1
            if functional_block:
                unit_2 = Unit.objects.get_or_create(
                    name=str.strip(functional_block),
                    parent=unit_1,
                    unit_type='функциональный блок'
                )[0]

            unit_3 = unit_2
            if unit_2_name:
                unit_3 = Unit.objects.get_or_create(
                    name=str.strip(unit_2_name),
                    parent=unit_2,
                    unit_type='подразделение'
                )[0]

            unit_4 = unit_3
            if unit_3_name:
                unit_4 = Unit.objects.get_or_create(
                    name=str.strip(unit_3_name),
                    parent=unit_3,
                    unit_type='подразделение'
                )[0]

            unit_5 = unit_4
            if unit_4_name:
                unit_5 = Unit.objects.get_or_create(
                    name=str.strip(unit_4_name),
                    parent=unit_4,
                    unit_type='подразделение'
                )[0]

            position = EmployeePosition.objects.get_or_create(
                name=str.strip(position_name),
                employee_role=str.strip(role)
            )[0]

            Employee.objects.create(
                unit=unit_5,
                position=position,
                first_name=str.strip(first_name),
                last_name=str.strip(last_name),
                phone=phone,
                city=city,
                address=address,
                email=email
            )