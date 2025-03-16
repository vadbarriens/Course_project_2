from typing import List

from src.hh_api import HeadHunterAPI
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


def user_interaction() -> None:
    """
    Функция для взаимодействия с пользователем.
    Запрашивает у пользователя поисковый запрос, количество вакансий для вывода и ключевые слова для фильтрации.
    Получает вакансии с hh.ru, фильтрует, сортирует и выводит их.
    """
    hh_api = HeadHunterAPI()
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()

    # Получаем вакансии с hh.ru
    hh_vacancies = hh_api.get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    # Фильтруем, сортируем и получаем топ-N вакансий
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Выводим вакансии
    print_vacancies(top_vacancies)

    # Сохраняем вакансии в JSON-файл
    json_saver = JSONSaver()
    for vacancy in top_vacancies:
        json_saver.add_vacancy(vacancy.__dict__)  # Преобразуем объект Vacancy в словарь


def filter_vacancies(
    vacancies: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """Фильтрует вакансии по ключевым словам в описании."""
    return [v for v in vacancies if all(word in v.description for word in filter_words)]


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортирует вакансии по зарплате (по убыванию)."""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Возвращает топ-N вакансий из списка."""
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Выводит информацию о вакансиях в консоль."""
    for vacancy in vacancies:
        print(f"{vacancy.name} - {vacancy.salary} - {vacancy.url}")


if __name__ == "__main__":
    user_interaction()
