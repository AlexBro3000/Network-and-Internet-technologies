import sqlite3
import pandas as pd


class TableDatabase:
    @staticmethod
    def create_tables(conn):
        cursor = conn.cursor()
        create_table_directors(cursor)  # Создание таблицы режиссёров
        create_table_actors(cursor)  # Создание таблицы актеров
        create_table_genres(cursor)  # Создание таблицы жанров
        create_table_movies(cursor)  # Создание таблицы фильмов
        create_table_halls(cursor)  # Создание таблицы залов
        create_table_seat_categories(cursor)  # Создание таблицы категорий мест
        create_table_sessions(cursor)  # Создание таблицы сеансов
        create_table_movies_actors(cursor)  # Создание связи между фильмами и актерами
        create_table_movies_genres(cursor)  # Создание связи между фильмами и жанрами
        create_table_halls_seat_categories(cursor)  # Создание связи между залами и категориями мест
        create_table_tickets(cursor)  # Создание таблицы билетов
        conn.commit()

    @staticmethod
    def fill_out_tables(conn):
        cursor = conn.cursor()
        fill_out_table_directors(conn, cursor)  # Заполнение таблицы режиссёров
        fill_out_table_actors(conn, cursor)  # Заполнение таблицы актеров
        fill_out_table_genres(conn, cursor)  # Заполнение таблицы жанров
        fill_out_table_movies(conn, cursor)  # Заполнение таблицы фильмов
        fill_out_table_halls(conn, cursor)  # Заполнение таблицы залов
        fill_out_table_seat_categories(conn, cursor)  # Заполнение таблицы категорий мест
        fill_out_table_sessions(conn, cursor)  # Заполнение таблицы сеансов
        fill_out_table_movies_actors(conn, cursor)  # Заполнение связи между фильмами и актерами
        fill_out_table_movies_genres(conn, cursor)  # Заполнение связи между фильмами и жанрами
        fill_out_table_halls_seat_categories(conn, cursor)  # Заполнение связи между залами и категориями мест
        conn.commit()

        cursor = conn.cursor()
        fill_out_table_tickets(conn, cursor)  # Заполнение таблицы билетов
        conn.commit()

    @staticmethod
    def get_table(conn, table):
        result_table = []
        for tbl in table:
            result_table.append({
                "name": tbl,
                "table": pd.read_sql("SELECT * FROM " + tbl, conn)
            })
        return result_table

    @staticmethod
    def is_table_empty(conn, table_name):
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        return row_count == 0


def create_table_directors(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Directors (
            director_id INTEGER PRIMARY KEY AUTOINCREMENT,
            director_full_name VARCHAR(50) NOT NULL
        );
    """)


def create_table_actors(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Actors (
            actor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            actor_full_name VARCHAR(50) NOT NULL
        );
    """)


def create_table_genres(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Genres (
            genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
            genre_name VARCHAR(20) NOT NULL
        );
    """)


def create_table_movies(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Movies (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_title VARCHAR(50) NOT NULL,
            movie_description VARCHAR(400),
            movie_img VARCHAR(50),
            director_id INTEGER,
            duration INTEGER,
            rating REAL,
            FOREIGN KEY (director_id) REFERENCES Directors(director_id)
        );
    """)


def create_table_halls(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Halls (
            hall_id INTEGER PRIMARY KEY AUTOINCREMENT,
            hall_name VARCHAR(20) NOT NULL
        );
    """)


def create_table_seat_categories(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SeatCategories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(20) NOT NULL,
            category_description VARCHAR(200)
        );
    """)


def create_table_sessions(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER,
            hall_id INTEGER,
            date DATE,
            start_time TIME,
            end_time TIME,
            FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
            FOREIGN KEY (hall_id) REFERENCES Halls(hall_id)
        );
    """)


def create_table_movies_actors(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MoviesActors (
            movie_id INTEGER,
            actor_id INTEGER,
            PRIMARY KEY (movie_id, actor_id),
            FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
            FOREIGN KEY (actor_id) REFERENCES Actors(actor_id)
        );
    """)


def create_table_movies_genres(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MoviesGenres (
            movie_id INTEGER,
            genre_id INTEGER,
            PRIMARY KEY (movie_id, genre_id),
            FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
            FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
        );
    """)


def create_table_halls_seat_categories(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS HallsSeatCategories (
            hall_id INTEGER,
            category_id INTEGER,
            number_seats INTEGER,
            PRIMARY KEY (hall_id, category_id),
            FOREIGN KEY (hall_id) REFERENCES Halls(hall_id),
            FOREIGN KEY (category_id) REFERENCES SeatCategories(category_id)
        );
    """)


def create_table_tickets(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tickets (
            session_id INTEGER,
            category_id INTEGER,
            available_seats INTEGER,
            price REAL,
            PRIMARY KEY (session_id, category_id),
            FOREIGN KEY (session_id) REFERENCES Sessions(session_id),
            FOREIGN KEY (category_id) REFERENCES SeatCategories(category_id)
        );
    """)


def fill_out_table_directors(conn, cursor):
    if TableDatabase.is_table_empty(conn, "Directors"):
        cursor.execute("""
            INSERT INTO Directors (director_full_name) VALUES
                ("Кристиан Риверс"),
                ("Роланд Эммерих"),
                ("Джим Хенсон");
        """)


def fill_out_table_actors(conn, cursor):
    if TableDatabase.is_table_empty(conn, "Actors"):
        cursor.execute("""
            INSERT INTO Actors (actor_full_name) VALUES
                ("Колин Сэлмон"),
                ("Лейла Джордж"),
                ("Марк Митчинсон"),
                ("Ронан Рафтери"),
                ("Стивен Лэнг"),
                ("Хьюго Уивинг"),
                ("Барбара Стил"),
                ("Джейсон Флеминг"),
                ("Мика Бурем"),
                ("Оуэн МакДоннелл"),
                ("Стив Уолл"),
                ("Сэм Эсхёрст"),
                ("Ванесса Редгрейв"),
                ("Дэвид Тьюлис"),
                ("Завьер Сэмюэл"),
                ("Рейф Сполл"),
                ("Себастьян Арместо"),
                ("Эдвард Хогг"),
                ("Гленн Пламмер"),
                ("Деннис Куэйд"),
                ("Джейк Джилленхол"),
                ("Кеннет Уэлш"),
                ("Села Уорд"),
                ("Эдриан Лестер"),
                ("Брайан Хенсон"),
                ("Дженнифер Коннелли"),
                ("Кристофер Малкольм"),
                ("Натали Финленд"),
                ("Шари Уайзер"),
                ("Шелли Томпсон");
        """)


def fill_out_table_genres(conn, cursor):
    if TableDatabase.is_table_empty(conn, "Genres"):
        cursor.execute("""
            INSERT INTO Genres (genre_name) VALUES
                ("Боевик"),
                ("Приключения"),
                ("Триллер"),
                ("Фантастика"),
                ("Фэнтези"),
                ("Ужасы"),
                ("Драма"),
                ("Семейный");
        """)


def fill_out_table_movies(conn, cursor):
    if TableDatabase.is_table_empty(conn, "Movies"):
        cursor.execute("""
            INSERT INTO Movies (movie_title, movie_description, movie_img, director_id, duration, rating) VALUES
                (
                    "Хроники хищных городов",
                    "Прошли тысячелетия после того, как мир настиг апокалипсис. Человечество адаптировалось и теперь живет по новым правилам. Гигантские движущиеся мегаполисы рассекают пустоши и поглощают маленькие города ради ресурсов. Том Нэтсуорти из нижнего уровня великого Лондона оказывается в смертельной опасности, когда на его пути появляется скрывающаяся от закона бунтарка Эстер Шоу. Они не должны были встретиться, но им суждено изменить будущее.",
                    "chronicles-of-predatory-cities.png", 1, 128, 6.2
                ),
                (
                    "Несколько минут после полуночи",
                    "После полуночи на земле воцаряется ужас в самых разных своих проявлениях. Демоны, каннибалы, убийцы, призраки и монстры заполоняют мир... В картине представлено девять мини-историй.",
                    "a-few-minutes-after-midnight.png", 1, 98, 5.1
                ),
                (
                    "Аноним",
                    "Фильм даст совершенно неожиданный ответ на извечный вопрос: а кем же «был или не был» Шекспир, и кто на самом деле скрывается за этим всемирно известным именем великого человека?",
                    "anonymous.png", 2, 130, 7.5
                ),
                (
                    "Послезавтра",
                    "Земля уверенно движется навстречу глобальной экологической катастрофе: в одной части света все живое погибает от засухи, в другой - разбушевавшаяся водная стихия сносит города.\nБлизость катастрофы вынуждает ученого-климатолога, пытающегося найти способ остановить глобальное потепление, отправиться на поиски пропавшего сына в Нью-Йорк, в котором наступил новый ледниковый период…",
                    "day-after-tomorrow.png", 2, 124, 7.7
                ),
                (
                    "Лабиринт",
                    "За гранью сна и яви, в полной удивительных чудес волшебной стране жил да был король гоблинов Джарет. Однажды услыхал он, как девочка Сара в сердцах сказала несносному младшему брату Тоби: «Чтоб тебя гоблины унесли!», — и тут же поймал ее на слове, утащив малыша в свой замок. Сара бросилась за Джаретом, пока дверь в сказку не захлопнулась.\nНо чтобы попасть в замок похитителя и спасти брата, ей придется пройти зачарованный Лабиринт. Он полон всяких чудищ, хитрых ловушек и головоломок. А выход из него стережет целая армия гоблинов! Встречая на своем пути сонмы невиданных созданий и разгадывая странные загадки, Сара храбро углубляется в таинственный мир Лабиринта.",
                    "labyrinth.png", 3, 101, 7.7
                );
        """)


def fill_out_table_halls(conn, cursor):
    if TableDatabase.is_table_empty(conn, "Halls"):
        cursor.execute("""
            INSERT INTO Halls (hall_name) VALUES
                ("Зал 1 - 2D/3D"),
                ("Зал 2 - 2D/3D"),
                ("Зал 3 - 2D/3D"),
                ("Зал 4 - 2D/3D"),
                ("Зал 5 - VIP"),
                ("Зал 6 - VIP"),
                ("Зал 7 - D-BOX"),
                ("Зал 8 - VIP D-BOX");
    """)


def fill_out_table_seat_categories(conn, cursor):
    if TableDatabase.is_table_empty(conn, "SeatCategories"):
        cursor.execute("""
            INSERT INTO SeatCategories (category_name, category_description) VALUES
                (
                    "Эконом",
                    "Места в первых рядах - не очень удобные для просмотра"
                ),
                (
                    "Стандарт",
                    "Стандартные места - выгодные по цене и удобные для просмотра"
                ),
                (
                    "Комфорт",
                    "Места в  центре зала - самые лучшие для комфортного просмотра"
                ),
                (
                    "VIP",
                    "Все места в VIP-залах - суперкомфортные кресла-реклайнеры"
                ),
                (
                    "VIP D-BOX",
                    "Динамические кресла D-BOX в VIP-залах"
                ),
                (
                    "D-BOX",
                    "Динамические кресла D-BOX"
                ),
                (
                    "Love",
                    "Парные диванчики  на последнем ряду для романтических свиданий"
                ),
                (
                    "Места для инвалидов",
                    "Специальные места для инвалидов-колясочников, не оборудованные креслом"
                );
        """)


def fill_out_table_sessions(conn, cursor):
    if TableDatabase.is_table_empty(conn, "Sessions"):
        cursor.execute("""
            INSERT INTO Sessions (movie_id, hall_id, date, start_time, end_time) VALUES
                (1, 1, '2020-01-01', '08:00', '10:30'),
                (1, 4, '2020-01-01', '10:30', '13:00'),
                (1, 1, '2020-01-01', '14:30', '17:00'),
                (1, 1, '2020-01-01', '17:00', '19:30'),
                (2, 2, '2020-01-01', '08:00', '10:00'),
                (2, 1, '2020-01-01', '10:30', '12:30'),
                (2, 1, '2020-01-01', '12:30', '14:30'),
                (2, 2, '2020-01-01', '14:30', '16:30'),
                (3, 3, '2020-01-01', '08:00', '10:30'),
                (3, 2, '2020-01-01', '12:00', '14:30'),
                (3, 3, '2020-01-01', '15:30', '18:00'),
                (3, 3, '2020-01-01', '18:00', '19:30'),
                (4, 4, '2020-01-01', '08:00', '10:30'),
                (4, 3, '2020-01-01', '10:30', '13:00'),
                (4, 3, '2020-01-01', '13:00', '15:30'),
                (4, 2, '2020-01-01', '16:30', '19:00'),
                (4, 4, '2020-01-01', '18:00', '19:30'),
                (5, 2, '2020-01-01', '10:00', '12:00'),
                (5, 4, '2020-01-01', '13:00', '15:30'),
                (5, 4, '2020-01-01', '15:30', '18:00'),
                
                (1, 1, '2020-01-02', '08:00', '10:30'),
                (1, 2, '2020-01-02', '10:00', '12:00'),
                (1, 1, '2020-01-02', '15:00', '17:30'),
                (1, 2, '2020-01-02', '17:00', '19:30'),
                (2, 2, '2020-01-02', '08:00', '10:00'),
                (2, 3, '2020-01-02', '10:30', '12:30'),
                (2, 3, '2020-01-02', '12:30', '14:30'),
                (2, 4, '2020-01-02', '15:30', '17:30'),
                (3, 3, '2020-01-02', '08:00', '10:30'),
                (3, 1, '2020-01-02', '12:30', '15:00'),
                (3, 2, '2020-01-02', '14:30', '17:00'),
                (3, 3, '2020-01-02', '16:30', '19:00'),
                (4, 4, '2020-01-02', '08:00', '10:30'),
                (4, 4, '2020-01-02', '10:30', '13:00'),
                (4, 4, '2020-01-02', '13:00', '15:30'),
                (4, 1, '2020-01-02', '17:30', '20:00'),
                (5, 1, '2020-01-02', '10:30', '12:30'),
                (5, 2, '2020-01-02', '12:30', '14:30'),
                (5, 3, '2020-01-02', '14:30', '16:30'),
                (5, 4, '2020-01-02', '17:30', '19:30');
    """)


def fill_out_table_movies_actors(conn, cursor):
    if TableDatabase.is_table_empty(conn, "MoviesActors"):
        cursor.execute("""
            INSERT INTO MoviesActors (movie_id, actor_id) VALUES
                (1, 1),
                (1, 2),
                (1, 3),
                (1, 4),
                (1, 5),
                (1, 6),
                (2, 7),
                (2, 8),
                (2, 9),
                (2, 10),
                (2, 11),
                (2, 12),
                (3, 13),
                (3, 14),
                (3, 15),
                (3, 16),
                (3, 17),
                (3, 18),
                (4, 19),
                (4, 20),
                (4, 21),
                (4, 22),
                (4, 23),
                (4, 24),
                (5, 25),
                (5, 26),
                (5, 27),
                (5, 28),
                (5, 29),
                (5, 30);
        """)


def fill_out_table_movies_genres(conn, cursor):
    if TableDatabase.is_table_empty(conn, "MoviesGenres"):
        cursor.execute("""
            INSERT INTO MoviesGenres (movie_id, genre_id) VALUES
                (1, 1),
                (1, 2),
                (1, 3),
                (1, 4),
                (1, 5),
                (2, 3),
                (2, 6),
                (3, 3),
                (3, 7),
                (4, 2),
                (4, 3),
                (4, 4),
                (4, 7),
                (5, 2),
                (5, 5),
                (5, 8);
        """)


def fill_out_table_halls_seat_categories(conn, cursor):
    if TableDatabase.is_table_empty(conn, "HallsSeatCategories"):
        cursor.execute("""
            INSERT INTO HallsSeatCategories (hall_id, category_id, number_seats) VALUES
                (1, 1, 12),
                (1, 2, 36),
                (1, 3, 12),
                (2, 1, 12),
                (2, 2, 36),
                (2, 3, 12),
                (3, 1, 30),
                (3, 2, 78),
                (3, 3, 28),
                (3, 7, 8),
                (3, 8, 12),
                (4, 1, 30),
                (4, 2, 78),
                (4, 3, 28),
                (4, 7, 8),
                (4, 8, 12),
                (5, 4, 80),
                (5, 7, 10),
                (6, 4, 120),
                (6, 7, 16),
                (7, 6, 80),
                (8, 5, 40);
        """)


def fill_out_table_tickets(conn, cursor):
    if TableDatabase.is_table_empty(conn, "Tickets"):
        sessions = pd.read_sql("""
            SELECT
                Session.session_id      AS 'session',
                HallsSeat.category_id   AS 'category',
                HallsSeat.number_seats  AS 'number'
            FROM Sessions AS 'Session'
                JOIN HallsSeatCategories AS 'HallsSeat' USING (hall_id)
        """, conn)

        for i in range(len(sessions)):
            session = int(sessions.loc[i, "session"])
            category = int(sessions.loc[i, "category"])
            seats = int(sessions.loc[i, "number"])
            price = 0
            match category:
                case 1:
                    price = 200
                case 2:
                    price = 320
                case 3:
                    price = 400
                case 4:
                    price = 560
                case 5:
                    price = 800
                case 6:
                    price = 600
                case 7:
                    price = 420
                case 8:
                    price = 160

            cursor.execute(f"""
                INSERT INTO Tickets (session_id, category_id, available_seats, price) VALUES
                    ({session}, {category}, {seats}, {price});
            """)