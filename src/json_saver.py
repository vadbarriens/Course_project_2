import json
import os
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List


class FileSaver(ABC):
    """Абстрактный класс для работы с файлами, содержащими вакансии.
    Определяет методы для добавления, получения и удаления вакансий."""

    @abstractmethod
    def add_vacancy(self, vacancy: Any) -> None:
        """Добавляет вакансию в файл."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Callable[[Dict], bool]) -> List[Dict]:
        """Возвращает список вакансий, соответствующих критерию."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Any) -> None:
        """Удаляет вакансию из файла."""
        pass


class JSONSaver:
    """Класс для работы с JSON-файлами, содержащими вакансии."""

    def __init__(self, filename: str = "vacancies.json") -> None:
        """Инициализирует экземпляр JSONSaver."""
        self._filename = filename

    def add_vacancy(self, vacancy: Dict) -> None:
        """Добавляет вакансию в JSON-файл."""
        vacancies = self.get_vacancies(lambda v: True)  # Получаем все вакансии
        vacancies.append(vacancy)  # Добавляем новую вакансию

        # Сохраняем обновленный список в файл
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

    def get_vacancies(self, criteria: Callable[[Dict], bool]) -> List[Dict]:
        """Возвращает список вакансий, соответствующих критерию."""
        if not os.path.exists(self._filename):
            return []

        with open(self._filename, "r", encoding="utf-8") as file:
            try:
                vacancies = json.load(file)
            except json.JSONDecodeError:
                vacancies = []
            return [v for v in vacancies if criteria(v)]

    def delete_vacancy(self, vacancy: Dict) -> None:
        """Удаляет вакансию из JSON-файла."""
        if not os.path.exists(self._filename):
            return

        with open(self._filename, "r", encoding="utf-8") as file:
            try:
                vacancies = json.load(file)
            except json.JSONDecodeError:
                vacancies = []

        # Удаляем вакансию
        vacancies = [v for v in vacancies if v["url"] != vacancy["url"]]

        # Сохраняем обновленный список в файл
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)
