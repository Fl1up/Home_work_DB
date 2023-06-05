import requests


class HHApi:
    """Класс по парсингу hh.ru"""
    def __init__(self):
        self.base_url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, keyword, area_id):
        params = {
            'text': keyword,
            'area': area_id,
            'period': 30,
            'per_page': 100
        }
        response = requests.get(self.base_url, params=params)
        return response.json()['items']
