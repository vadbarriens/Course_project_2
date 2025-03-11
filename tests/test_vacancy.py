from src.vacancy import Vacancy


def test_vacancy_creation():
    vacancy = Vacancy(
        "Python Developer",
        "https://hh.ru/vacancy/123456",
        100000,
        "Требования: опыт работы от 3 лет...",
    )
    assert vacancy.name == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123456"
    assert vacancy.salary == 100000
    assert vacancy.description == "Требования: опыт работы от 3 лет..."


def test_vacancy_comparison():
    vacancy1 = Vacancy(
        "Python Developer",
        "https://hh.ru/vacancy/123456",
        100000,
        "Требования: опыт работы от 3 лет...",
    )
    vacancy2 = Vacancy(
        "Java Developer",
        "https://hh.ru/vacancy/654321",
        120000,
        "Требования: опыт работы от 5 лет...",
    )
    assert vacancy1 < vacancy2
    assert not (vacancy1 > vacancy2)
    assert not (vacancy1 == vacancy2)


def test_none_salary():
    vacancy = Vacancy(
        "Python Developer",
        "https://hh.ru/vacancy/123456",
        None,
        "Требования: опыт работы от 3 лет...",
    )
    assert vacancy.salary == 0  # Проверка, что зарплата по умолчанию равна 0


def test_none_description():
    vacancy = Vacancy("Python Developer", "https://hh.ru/vacancy/123456", 100000, None)
    assert vacancy.description == ""  # Проверка, что описание по умолчанию пустое
