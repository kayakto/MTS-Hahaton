import pandas as pd
import sqlite3

# 1. Чтение файла Excel
file_path = 'file.xlsx'  # Укажите путь к вашему файлу
data = pd.read_excel(file_path)

# Убираем лишние пробелы из названий столбцов
data.columns = data.columns.str.strip()

# 2. Подготовка данных
units = []
employees = []
positions = []
unit_ids = {}  # Словарь для хранения уникальных подразделений
employee_id = 1  # Счётчик для сотрудников
position_ids = {}  # Словарь для уникальных должностей

def add_unit(name, parent_name=None, unit_type=None):
    """Добавляет подразделение в units, если его ещё нет."""
    # Уникальное имя подразделения: name + parent_name
    unique_name = f"{name}_{parent_name}" if parent_name else name
    if unique_name not in unit_ids:
        unit_id = len(units) + 1
        parent_id = unit_ids.get(parent_name)
        units.append({
            "id": unit_id,
            "parent_unit_id": parent_id,
            "name": name,
            "unit_type": unit_type
        })
        unit_ids[unique_name] = unit_id
    return unit_ids[unique_name]

def add_position(position_name):
    """Добавляет должность в employee_positions, если её ещё нет."""
    if position_name not in position_ids:
        position_id = len(positions) + 1
        positions.append({
            "id": position_id,
            "name": position_name
        })
        position_ids[position_name] = position_id
    return position_ids[position_name]

# 3. Преобразование данных
for _, row in data.iterrows():
    # Если у подразделения 1 есть только подразделение 4, переместим его в подразделение 2
    if pd.notna(row['Подразделение 1']) and pd.notna(row['Подразделение 4']) and pd.isna(row['Подразделение 2']) and pd.isna(row['Подразделение 3']):
        row['Подразделение 2'] = row['Подразделение 4']
        row['Подразделение 4'] = None

    # Добавление подразделений
    unit1 = row['Подразделение 1']
    unit2 = row['Подразделение 2']
    unit3 = row['Подразделение 3']
    unit4 = row['Подразделение 4']
    unit_type = row['Функциональный блок']  # Учитываем функциональный блок

    if pd.notna(unit1):
        add_unit(unit1, None, unit_type)
    if pd.notna(unit2):
        add_unit(unit2, unit1, unit_type)
    if pd.notna(unit3):
        add_unit(unit3, unit2, unit_type)
    if pd.notna(unit4):
        add_unit(unit4, unit3, unit_type)

    # Добавление должности
    position_name = row['Должность']
    position_id = add_position(position_name)

    # Добавление сотрудника
    employees.append({
        "id": employee_id,
        "first_name": row['Имя'],
        "second_name": row['Фамилия'],
        "phone": row.get('Телефон'),
        "city": row.get('Город'),
        "address": row.get('Адрес'),
        "email": row.get('Email'),
        "unit_id": unit_ids.get(f"{unit4}_{unit3}_{unit2}_{unit1}" or f"{unit3}_{unit2}_{unit1}" or f"{unit2}_{unit1}" or unit1),
        "employee_position": position_id
    })
    employee_id += 1

# 4. Создание базы данных SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Таблица подразделений
cursor.execute('''
CREATE TABLE IF NOT EXISTS units (
    id INTEGER PRIMARY KEY,
    parent_unit_id INTEGER,
    name TEXT,
    unit_type TEXT,
    FOREIGN KEY(parent_unit_id) REFERENCES units(id)
)
''')

# Таблица должностей
cursor.execute('''
CREATE TABLE IF NOT EXISTS employee_positions (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')

# Таблица сотрудников
cursor.execute('''
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY,
    unit_id INTEGER,
    employee_position INTEGER,
    first_name TEXT,
    second_name TEXT,
    phone TEXT,
    city TEXT,
    address TEXT,
    email TEXT,
    FOREIGN KEY(unit_id) REFERENCES units(id),
    FOREIGN KEY(employee_position) REFERENCES employee_positions(id)
)
''')

# Загрузка данных в таблицы
cursor.executemany('''
INSERT INTO units (id, parent_unit_id, name, unit_type)
VALUES (:id, :parent_unit_id, :name, :unit_type)
''', units)

cursor.executemany('''
INSERT INTO employee_positions (id, name)
VALUES (:id, :name)
''', positions)

cursor.executemany('''
INSERT INTO employee (id, unit_id, employee_position, first_name, second_name, phone, city, address, email)
VALUES (:id, :unit_id, :employee_position, :first_name, :second_name, :phone, :city, :address, :email)
''', employees)

conn.commit()
conn.close()

print("Данные успешно загружены!")
