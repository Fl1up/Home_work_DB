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


def main():
    hh_api = HHApi()
    db_manager = DBManager()
    db_manager.drop()
    db_manager.create_tables()
    for company in companies:
        employer_id = db_manager.add_employer(company['name'], company['url'])
        vacancies = hh_api.get_vacancies(company['name'], 1)
        for vacancy in vacancies:
            db_manager.add_vacancy(vacancy['name'], vacancy["salary"], vacancy['alternate_url'], employer_id)

    while True:

        print("\nВведите интересующий вас запрос :\n"
              "1 - Вывести все выбранные компании :\n"
              "2 - Вывести количество вакансий у каждой компании :\n"
              "3 - Вывести среднюю заработную плату в компаниях :\n"
              "4 - Вывести заработную плату выше чем средняя по компаниям :\n"
              "5 - Вывести вакансии с нужным фильтром :\n"
              "Введите 'exit' для выхода :\n")

        inp = input()
        try:
            if inp == "1":
                for i in companies:
                    print(i["name"])
            elif inp == "2":
                for i in db_manager.get_companies_and_vacancies_count():
                    print(f"Компания : {i[0]}\nКоличество вакансий : {i[1]},")
            elif inp == "3":
                print(f"Средняя зарплата : {round(db_manager.get_avg_salary())}")
            elif inp == "4":
                for i in db_manager.get_vacancies_with_higher_salary():
                    print(f"Вакансия : {i[1]}\nЗаработная плата : {i[2]},")
            elif inp == "5":
                print("Введите слово по которому организовать поиск :")
                a = input()
                print(f"Происходит поиск по слову {a}")
                for i in db_manager.get_vacancies_with_keyword(a):
                    print(f"Вакансия : {i[1]}\nСсылка на вакансию : {i[3]},")
            else:
                print("Нет такого варианта")
        finally:
            if inp == "exit":
                print("Работа завершена")
                break

    db_manager.close()


main()
