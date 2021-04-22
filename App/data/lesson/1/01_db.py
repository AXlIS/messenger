# ------------------------------ Базы данных -----------------------------
# Импортируем библиотеку, соответствующую типу нашей базы данных
import sqlite3

from icecream import ic

# Создаем соединение с нашей базой данных
# В нашем примере у нас это просто файл базы
with sqlite3.connect("company.db3") as conn:
    conn.row_factory = sqlite3.Row
    # Создаем курсор - это специальный объект который делает запросы и получает их результаты
    cursor = conn.cursor()

    # ТУТ БУДЕТ НАШ КОД РАБОТЫ С БАЗОЙ ДАННЫХ
    # КОД ДАЛЬНЕЙШИХ ПРИМЕРОВ ВСТАВЛЯТЬ В ЭТО МЕСТО

    cursor.execute(
        """
                    create table if not exists Terminal (
                        id  INTEGER primary key,
                        title TEXT,
                        configuration TEXT
                    );
        """
    )

    try:
        cursor.execute(
            """
            insert into Terminal (id, title, configuration)
            VALUES (?, ?, ?);""",
            (13, "Terminal Bingo", '{"simle":"nothing"}'),
        )
    except sqlite3.IntegrityError:
        pass

    cursor.execute("SELECT * FROM Terminal where id = :id", {"id": 13})

    z = cursor.fetchone()
    while z:
        print(z)
        ic(z[0])
        ic(z[1])
        ic(z[2])
        z = cursor.fetchone()

    cursor.execute("SELECT * FROM Terminal where id = ?", (13,))
    for row in cursor:
        ic(row["id"])
        ic(row["title"])
        ic(row["configuration"])

    items = [(1, "aaa", "config1"), (100, "bbb", "config2")]
    try:
        cursor.executemany(
            """
            insert into Terminal (id, title, configuration)
            VALUES (?, ?, ?);""",
            items,
        )
    except sqlite3.IntegrityError:
        pass

    cursor.execute("SELECT * FROM Terminal")
    for row in cursor:
        for value in row:
            ic(value)

        print()

    cursor.executescript(
        """
        create table if not exists Terminal (
        id  INTEGER primary key,
        title TEXT,
        configuration TEXT
        );


        SELECT * FROM Terminal
        """
    )

    term_id = "13 OR 1 = 1"
    cursor.execute(f"SELECT * FROM Terminal where id = {term_id}")
    # cursor.execute("SELECT * FROM Terminal where id = ?", (term_id,))
    for row in cursor:
        ic(row)

# Не забываем закрыть соединение с базой данных
# conn.close()
