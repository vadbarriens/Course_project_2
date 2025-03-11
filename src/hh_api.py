from abc import ABC, abstractmethod
from typing import Dict, List

import requests


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями."""

    @abstractmethod
    def get_vacancies(self, query: str) -> List[Dict]:
        """Получает список вакансий по ключевому слову."""
        pass


class HeadHunterAPI(VacancyAPI):
    """
    Класс для работы с API HeadHunter.
    Реализует метод для получения вакансий с сайта hh.ru.
    """

    def __init__(self) -> None:
        """
        Инициализирует экземпляр класса HeadHunterAPI.
        Устанавливает базовый URL и параметры запроса.
        """
        self._url = "https://api.hh.ru/vacancies"  # Базовый URL API
        self._params: dict[str, str | int | float | None] = {
            "per_page": 100,
            "area": "113",
        }  # Параметры запроса по умолчанию

    def get_vacancies(self, query: str) -> List[Dict]:
        """Получает список вакансий с сайта hh.ru по ключевому слову."""
        self._params["text"] = query  # Добавляем ключевое слово в параметры запроса
        response = requests.get(self._url, params=self._params)

        # Проверяем статус ответа
        if response.status_code == 200:
            return response.json()["items"]  # Возвращаем список вакансий
        else:
            raise Exception(f"Ошибка при запросе к API: {response.status_code}")
