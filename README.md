В данной курсовой мы познакомились с PostgreSQL.
Научились создавать и редактировать таблицы.

Home_work_DB

В данном проекте мы создавали код для создания и заполнения данными таблиц по требованиям из задания

## Установка

Инструкции по установке PostgreSQL и необходимых библиотек для работы с ООП.

## Использование

Код из hh_api служит для создания класса для парсинга страниц по поиску работы. В данном случае hh.ru

Код из DBmanager служит для подключения и заполнение данными базы данных

## База данных

Основные команды

"""CREATE TABLE vacancies (тут должны быть условия и название столбцов)""") -- создание таблиц

"""INSERT INTO employers (name, url) VALUES (%s, %s) RETURNING id""", (name, url)  -- заполнение таблиц

"""SELECT employers.name, COUNT(vacancies.id) FROM employers LEFT JOIN vacancies ON employers. id = vacancies.employer_id
            GROUP BY employers.name"""   -- группировка  

"""SELECT employers.name, vacancies.name, vacancies.salary, vacancies.url 
            FROM vacancies 
            INNER JOIN employers ON vacancies.employer_id = employer_id """  -- заполнение таблиц

## Дополнительная информация

По всем интересующим вопросам, писать в личные сообщения 