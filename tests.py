import os
import pytest
import tempfile

from csv_reader import reader_csv, read_list_csv
from report_generate import detect_salary_id


# Фикстуры для тестовых данных
@pytest.fixture
def temp_csv_file():
    """Создаем временный CSV-файл для тестов"""
    content = """name,department,pay,age
Ivan,IT,100000,30
Petr,HR,80000,25"""

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def temp_csv_with_different_salary_name():
    """CSV с альтернативным названием колонки зарплаты"""
    content = """name,department,wage,age
Ivan,IT,100000,30
Petr,HR,80000,25"""

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)


def test_reader_csv_file_not_found(monkeypatch):
    """Тест обработки отсутствующего файла"""
    # Мокаем sys.exit чтобы проверить вызов
    with pytest.raises(SystemExit):
        reader_csv('nonexistent_file.csv')


def test_reader_csv_empty_file():
    """Тест с пустым CSV-файлом"""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv') as f:
        f.write("")  # Пустой файл
        f.flush()
        with pytest.raises(StopIteration):
            reader_csv(f.name)


def test_reader_csv_missing_salary_column():
    """Тест с отсутствующей колонкой зарплаты"""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv') as f:
        f.write("name,department,age\nIvan,IT,30")
        f.flush()
        with pytest.raises(ValueError):
            reader_csv(f.name)


# Параметризованные тесты
@pytest.mark.parametrize("content,expected_count", [
    ("name,pay\nIvan,100", 1),
    ("name,pay\nIvan,100\nPetr,200", 2),
    ("name,pay\nIvan,100\nPetr,200\nAlex,300", 3),
])
def test_reader_csv_row_count(content, expected_count):
    """Параметризованный тест количества строк"""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv') as f:
        f.write(content)
        f.flush()
        result = reader_csv(f.name)
        assert len(result) == expected_count


# Тесты для detect_salary_id
def test_detect_salary_id():
    """Тест функции определения колонки зарплаты"""
    assert detect_salary_id(['name', 'salary', 'age']) == 1
    assert detect_salary_id(['name', 'pay', 'age']) == 1
    assert detect_salary_id(['name', 'wage', 'age']) == 1
    assert detect_salary_id(['name', 'compensation', 'age']) == 1
    with pytest.raises(ValueError):
        detect_salary_id(['name', 'age'])  # Нет колонки зарплаты


# Фикстуры для тестовых CSV-файлов
@pytest.fixture
def temp_csv_file_1():
    """Первый тестовый CSV-файл"""
    content = "name,department,salary\nIvan,IT,100000\nPetr,HR,80000"
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def temp_csv_file_2():
    """Второй тестовый CSV-файл"""
    content = "name,department,salary\nAnna,IT,120000\nOlga,HR,85000"
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def temp_csv_file_3():
    """Третий тестовый CSV-файл с другим отделом"""
    content = "name,department,salary\nDmitry,Finance,150000"
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)


# Основные тесты
def test_read_list_csv_basic(temp_csv_file_1, temp_csv_file_2):
    """Тест базового объединения двух файлов"""
    result = read_list_csv([temp_csv_file_1, temp_csv_file_2])

    assert len(result) == 4
    assert result[0]['department'] == 'HR'
    assert result[1]['department'] == 'HR'
    assert result[2]['department'] == 'IT'
    assert result[3]['department'] == 'IT'


def test_read_list_csv_single_file(temp_csv_file_1):
    """Тест с одним файлом"""
    result = read_list_csv([temp_csv_file_1])

    assert len(result) == 2
    assert result[0]['department'] == 'HR'
    assert result[1]['department'] == 'IT'


def test_read_list_csv_multiple_departments(temp_csv_file_1, temp_csv_file_3):
    """Тест с разными отделами"""
    result = read_list_csv([temp_csv_file_1, temp_csv_file_3])

    assert len(result) == 3
    assert result[0]['department'] == 'Finance'
    assert result[1]['department'] == 'HR'
    assert result[2]['department'] == 'IT'


def test_read_list_csv_empty_input():
    """Тест с пустым списком файлов"""
    result = read_list_csv([])
    assert len(result) == 0
    assert isinstance(result, list)


# Тесты обработки ошибок
def test_read_list_csv_nonexistent_file():
    """Тест с несуществующим файлом"""
    with pytest.raises(SystemExit):
        read_list_csv(["nonexistent_file.csv"])


def test_read_list_csv_invalid_file():
    """Тест с некорректным CSV-файлом"""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv') as f:
        f.write("invalid,data\n1,2,3,4")  # Неправильный формат
        f.flush()
        with pytest.raises(ValueError):
            read_list_csv([f.name])


# Параметризованные тесты
@pytest.mark.parametrize("files_count", [1, 2, 3, 5])
def test_read_list_csv_various_file_counts(files_count):
    """Параметризованный тест разного количества файлов"""
    files = []
    try:
        for i in range(files_count):
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
                f.write(f"name,department,salary\nEmployee{i},Dept{i % 2},100000")
                f.flush()
                files.append(f.name)

        result = read_list_csv(files)
        assert len(result) == files_count
    finally:
        for f in files:
            os.unlink(f)


def test_read_list_csv_sorting_stability():
    """Тест стабильности сортировки (сохранение порядка записей с одинаковым отделом)"""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv') as f1, \
            tempfile.NamedTemporaryFile(mode='w+', suffix='.csv') as f2:
        # Создаем файлы с сотрудниками одного отдела
        f1.write("name,department,salary\nIvan,IT,100000\nPetr,IT,110000")
        f1.flush()
        f2.write("name,department,salary\nAnna,IT,120000\nOlga,IT,130000")
        f2.flush()

        result = read_list_csv([f1.name, f2.name])

        # Проверяем что порядок сохранен (первыми идут записи из первого файла)
        assert result[0]['name'] == 'Ivan'
        assert result[1]['name'] == 'Petr'
        assert result[2]['name'] == 'Anna'
        assert result[3]['name'] == 'Olga'