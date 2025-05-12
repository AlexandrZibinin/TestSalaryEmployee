from env_setting import STANDART_COLUMN

def detect_salary_id(column_data):
    """Определение индекса зарплаты в списке отчета"""
    data_copy = list(column_data)
    salary_name = list(set(data_copy) - STANDART_COLUMN)
    result = None
    for column_num in range(len(data_copy)):
        if data_copy[column_num].lower() == salary_name[0]:
            result = column_num
    return result

def print_payouts_report(all_data_employers):
    """Вывод данных по работникам в таблице"""
    headers = ['Отдел', 'Имя', 'Наработка', 'Ставка', 'К выплате']
    rows = []
    for employee in all_data_employers:
        payout = int(employee.get('hours_worked')) * int(employee.get('salary'))
        rows.append(
            [
                employee.get('department'),
            employee.get('name'),
            employee.get('hours_worked'),
            f'${employee.get('salary')}',
            f'${payout}'
            ]
        )
    """Оформление таблицы"""
    col_widths = [
        max(len(str(row[i])) for row in [headers] + rows)
        for i in range(len(headers))
    ]

    separator = '+' + '+'.join(['-' * (width + 2) for width in col_widths]) + '+'

    print(separator)

    header_row = '| ' + ' | '.join(
        f"{header:<{col_widths[i]}}" for i, header in enumerate(headers)
    ) + ' |'
    print(header_row)
    print(separator)

    for row in rows:
        data_row = '| ' + ' | '.join(
            f"{str(item):<{col_widths[i]}}" for i, item in enumerate(row)
        ) + ' |'
        print(data_row)

    print(separator)
