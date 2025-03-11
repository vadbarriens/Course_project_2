import json

import pytest

from src.json_saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def json_saver(tmpdir):
    # Используем временный файл для тестов
    filename = tmpdir.join("test_vacancies.json")
    return JSONSaver(filename=str(filename))


def test_add_vacancy(json_saver):
    vacancy = Vacancy(
        "Python Developer",
        "https://hh.ru/vacancy/123456",
        100000,
        "Требования: опыт работы от 3 лет...",
    )
    json_saver.add_vacancy(vacancy.__dict__)  # Передаем словарь

    # Проверяем, что файл содержит добавленную вакансию
    with open(json_saver._filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        assert len(data) == 1
        assert data[0]["name"] == "Python Developer"
        assert data[0]["url"] == "https://hh.ru/vacancy/123456"
        assert data[0]["salary"] == 100000
        assert data[0]["description"] == "Требования: опыт работы от 3 лет..."


def test_get_vacancies(json_saver):
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
    json_saver.add_vacancy(vacancy1.__dict__)  # Передаем словарь
    json_saver.add_vacancy(vacancy2.__dict__)  # Передаем словарь

    # Получаем вакансии с зарплатой больше 100000
    criteria = lambda v: v["salary"] > 100000
    vacancies = json_saver.get_vacancies(criteria)

    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Java Developer"


def test_delete_vacancy(json_saver):
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
    json_saver.add_vacancy(vacancy1.__dict__)  # Передаем словарь
    json_saver.add_vacancy(vacancy2.__dict__)  # Передаем словарь

    # Удаляем вакансию Python Developer
    json_saver.delete_vacancy(vacancy1.__dict__)

    # Проверяем, что осталась только одна вакансия
    with open(json_saver._filename, "r", encoding="utf-8") as file:
        vacancies = json.load(file)
        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Java Developer"


def test_empty_file(json_saver):
    # Проверяем, что get_vacancies возвращает пустой список для пустого файла
    vacancies = json_saver.get_vacancies(lambda v: True)
    assert len(vacancies) == 0


def test_delete_nonexistent_vacancy(json_saver):
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
    json_saver.add_vacancy(vacancy1.__dict__)  # Передаем словарь

    # Пытаемся удалить вакансию, которой нет в файле
    json_saver.delete_vacancy(vacancy2.__dict__)

    # Проверяем, что файл не изменился
    with open(json_saver._filename, "r", encoding="utf-8") as file:
        vacancies = json.load(file)
        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"