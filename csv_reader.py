import os
import sys

from env_setting import DATA_FOLDER
from report_generate import detect_salary_id

def reader_csv(filename):
    """Чтение CSV-файла + приведение колонки зарплаты к общему названию"""
    data = []
    try:
        with open(os.path.join(DATA_FOLDER, filename), 'r', encoding='utf-8') as file:
            headers = file.readline().strip().split(',')
            salary_name = detect_salary_id(headers)
            headers[salary_name] = "salary"
            for line in file:
                row = line.strip().split(',')
                employee = dict(zip(headers, row))
                data.append(employee)
        return data
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден!")
        sys.exit(1)

def read_list_csv(files):
    """Принимает список файлов из парсера и выводит отсортированные по отделам данные в общий файл по всем отчетам"""
    result = []
    for file in files:
        data = reader_csv(file)
        for line in data:
            result.append(line)
    sorted_result = sorted(result, key=lambda x: x['department'])
    return sorted_result


