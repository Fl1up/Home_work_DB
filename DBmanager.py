import psycopg2


class DBManager:
    """Класс подключение к бд заполнение ее и фильтрация"""
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", database="north_data", user="postgres")
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.cur.execute("""CREATE TABLE employers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        url VARCHAR(255) NOT NULL)""")
        self.conn.commit()  # Создание бд компании и вакансии

        self.cur.execute("""
        CREATE TABLE vacancies (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        salary varchar(255) ,
        url VARCHAR(255) NOT NULL,
        employer_id INTEGER NOT NULL,
        FOREIGN KEY (employer_id) REFERENCES employers (id))""")
        self.conn.commit()

    def add_employer(self, name, url): # заполнение таблиц компании
        self.cur.execute("""INSERT INTO employers (name, url) VALUES (%s, %s) RETURNING id""", (name, url))
        employer_id = self.cur.fetchone()[0]
        self.conn.commit()
        return employer_id

    def add_vacancy(self, name, salary, url, employer_id):  # заполнение таблиц вакансии по параметрам
        if salary is not None:
            self.cur.execute("""INSERT INTO vacancies (name, salary, url, employer_id) VALUES (%s, %s, %s, %s)""", (name, salary["from"], url, employer_id))
        else:
            self.cur.execute("""INSERT INTO vacancies (name, salary, url, employer_id) VALUES (%s, %s, %s, %s)""", (name, None, url, employer_id))
        self.conn.commit()

    def get_companies_and_vacancies_count(self):  # количество вакансий у компаний
        self.cur.execute("""SELECT employers.name, COUNT(vacancies.id) FROM employers LEFT JOIN vacancies ON employers.id = vacancies.employer_id
            GROUP BY employers.name""")
        result = self.cur.fetchall()
        return result

    def get_all_vacancies(self):  # функция вывода компании вакансий зп и ссылке
        self.cur.execute("""SELECT  employers.name, vacancies.name, vacancies.salary, vacancies.url 
            FROM vacancies 
            INNER JOIN employers ON vacancies.employer_id = employer_id """)
        result = self.cur.fetchall()
        vacancies = []
        for row in result:
            vacancy = {
                "employer_name": row[0],
                "vacancy_name": row[1],
                "salary": row[2],
                "url": row[3]
            }
            vacancies.append(vacancy)
        return vacancies

    def get_avg_salary(self):  # функция поиска средней зп
        self.cur.execute("""SELECT AVG(CAST(salary AS numeric)) FROM vacancies""")
        result = self.cur.fetchone()[0]
        return result

    def get_vacancies_with_higher_salary(self):  # поиск вакансии по средней зп и фильтрации выше нее
        self.cur.execute("""SELECT AVG(CAST(salary AS numeric)) FROM vacancies""")
        avg_salary = self.cur.fetchone()[0]
        self.cur.execute(f"""SELECT * FROM vacancies WHERE CAST(salary AS numeric) > {avg_salary}""")
        result = self.cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, word):
        self.cur.execute(f"SELECT * FROM vacancies WHERE name LIKE '{word}%'")
        result = self.cur.fetchall()
        return result
    def drop(self):  # функция для перезапуска без удаления бд в редакторе бд
        self.cur.execute("""DROP TABLE vacancies,employers""")
        self.conn.commit()

    def close(self):  # функция закрытия соединения с бд
        self.cur.close()
        self.conn.close()
