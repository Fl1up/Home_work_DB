from DBmanager import DBManager
from hh_api import HHApi

companies = [
    {'name': 'Яндекс', 'url': 'https://yandex.ru/jobs/'},
    {'name': 'Mail.ru Group', 'url': 'https://corp.mail.ru/ru/career/'},
    {'name': 'Сбербанк', 'url': 'https://sbercareers.ru/'},
    {'name': 'Tinkoff', 'url': 'https://www.tinkoff.ru/career/'},
    {'name': 'Ozon', 'url': 'https://company.ozon.ru/jobs/'},
    {'name': 'Wildberries', 'url': 'https://corp.wildberries.ru/jobs/'},
    {'name': 'Avito', 'url': 'https://www.avito.ru/career'},
    {'name': 'EPAM', 'url': 'https://www.epam.com/careers'},
    {'name': 'Luxoft', 'url': 'https://career.luxoft.com/'},
    {'name': 'Alfa-Bank', 'url': 'https://alfabank.ru/career/vacancies/'}]

hh_api = HHApi()
db_manager = DBManager('localhost', 'home_work', 'postgres')
db_manager.drop()
db_manager.create_tables()
for company in companies:
    employer_id = db_manager.add_employer(company['name'], company['url'])
    vacancies = hh_api.get_vacancies(company['name'], 1)
    for vacancy in vacancies:
        db_manager.add_vacancy(vacancy['name'], vacancy["salary"], vacancy['alternate_url'], employer_id)

db_manager.get_vacancies_with_keyword()


db_manager.close()

