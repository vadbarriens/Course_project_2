import pytest
import requests_mock

from src.hh_api import HeadHunterAPI


def test_get_vacancies_success():
    hh_api = HeadHunterAPI()
    mock_response = {
        "items": [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123456",
            },
            {"name": "Java Developer", "alternate_url": "https://hh.ru/vacancy/654321"},
        ]
    }
    with requests_mock.Mocker() as m:
        m.get("https://api.hh.ru/vacancies", json=mock_response, status_code=200)
        vacancies = hh_api.get_vacancies("Python")
        assert len(vacancies) == 2
        assert vacancies[0]["name"] == "Python Developer"
        assert vacancies[1]["name"] == "Java Developer"


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (400, "Ошибка при запросе к API: 400"),
        (404, "Ошибка при запросе к API: 404"),
        (500, "Ошибка при запросе к API: 500"),
    ],
)
def test_get_vacancies_failure(status_code, expected_error):
    hh_api = HeadHunterAPI()
    with requests_mock.Mocker() as m:
        m.get("https://api.hh.ru/vacancies", status_code=status_code)
        with pytest.raises(Exception, match=expected_error):
            hh_api.get_vacancies("Python")


def test_get_vacancies_query_params():
    hh_api = HeadHunterAPI()
    with requests_mock.Mocker() as m:
        m.get("https://api.hh.ru/vacancies", json={"items": []}, status_code=200)
        hh_api.get_vacancies("Python")
        assert m.last_request.qs == {
            "text": ["python"],
            "area": ["113"],
            "per_page": ["100"],
        }