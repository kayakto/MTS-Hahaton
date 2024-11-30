import openpyxl
from django.db import transaction
from .models import *


def parse_excel_and_save_to_db(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    if Unit.objects.count() > 0:
        print("Db is already parsed")
        return

    with transaction.atomic():
        for row in sheet.iter_rows(min_row=2, values_only=True):
            unit_1_name = str.strip(row[0])
            functional_block = str.strip(row[1])
            unit_2_name = str.strip(row[2])
            unit_3_name = str.strip(row[3])
            unit_4_name = str.strip(row[4])
            position_name = str.strip(row[5])
            role = str.strip(row[6])
            last_name = str.strip(row[7])
            first_name = str.strip(row[8])
            phone = str.strip(row[9])
            city = str.strip(row[10])
            address = str.strip(row[11])
            email = str.strip(row[12])

            if not unit_1_name:
                continue

            unit_1 = Unit.objects.get_or_create(
                name=unit_1_name,
                parent=None,
                unit_type='division'
            )[0]

            unit_2 = unit_1
            if functional_block:
                unit_2 = Unit.objects.get_or_create(
                    name=functional_block,
                    parent=unit_1,
                    unit_type='functional_unit'
                )[0]

            unit_3 = unit_2
            if unit_2_name:
                unit_3 = Unit.objects.get_or_create(
                    name=unit_2_name,
                    parent=unit_2,
                    unit_type='division'
                )[0]

            unit_4 = unit_3
            if unit_3_name:
                unit_4 = Unit.objects.get_or_create(
                    name=unit_3_name,
                    parent=unit_3,
                    unit_type='division'
                )[0]

            unit_5 = unit_4
            if unit_4_name:
                unit_5 = Unit.objects.get_or_create(
                    name=unit_4_name,
                    parent=unit_4,
                    unit_type='division'
                )[0]

            position = EmployeePosition.objects.get_or_create(
                name=position_name,
                employee_role=role
            )[0]

            Employee.objects.create(
                unit=unit_5,
                position=position,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                city=city,
                address=address,
                email=email
            )