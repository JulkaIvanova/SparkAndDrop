import os
import sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'data', 'game')

expected_structure = {
    'users': {
        'levelOne_complite': 'INTEGER',
        'levelTwo_complite': 'INTEGER',
        'levelThree_complite': 'INTEGER',
        'levelFour_complite': 'INTEGER',
        'total_complite': 'INTEGER'
    },
    'levelOne': {'time': 'REAL', 'coins': 'INTEGER'},
    'levelTwo': {'time': 'REAL', 'coins': 'INTEGER'},
    'levelThree': {'time': 'REAL', 'coins': 'INTEGER'},
    'levelFour': {'time': 'REAL', 'coins': 'INTEGER'}
}


def get_db_structure(cursor):
    structure = {}
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        structure[table] = {row[1]: row[2] for row in cursor.fetchall()}
    return structure


def validate_and_fix_data(cursor):
    for table, columns in expected_structure.items():
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        for row in rows:
            update_values = {}
            for col, dtype in columns.items():
                value = row[list(columns.keys()).index(col)]
                if dtype == 'INTEGER' and not isinstance(value, int):
                    update_values[col] = 0
                elif dtype == 'REAL' and not isinstance(value, float):
                    update_values[col] = 0.0
            if update_values:
                set_clause = ', '.join(f"{col} = ?" for col in update_values.keys())
                cursor.execute(f"UPDATE {table} SET {set_clause} WHERE rowid = ?",
                               list(update_values.values()) + [row[0]])
        if table == 'users' and not rows:
            cursor.execute(
                "INSERT INTO users (levelOne_complite, levelTwo_complite, levelThree_complite, levelFour_complite,"
                " total_complite) VALUES (0, 0, 0, 0, 0)")
    cursor.execute("""
        UPDATE users 
        SET total_complite = levelOne_complite + levelTwo_complite + levelThree_complite + levelFour_complite
    """)

    cursor.connection.commit()


def create_database():
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for table, columns in expected_structure.items():
            columns_str = ', '.join(f'{col} {dtype}' for col, dtype in columns.items())
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns_str})")
        cursor.execute(
            "INSERT INTO users (levelOne_complite, levelTwo_complite, levelThree_complite, levelFour_complite,"
            " total_complite) VALUES (0, 0, 0, 0, 0)")
        conn.commit()


def reset_database():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = OFF")
        for table in get_db_structure(cursor).keys():
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
        create_database()


def check_and_update_database():
    if not os.path.exists(db_path):
        create_database()
        return
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        current_structure = get_db_structure(cursor)
        if current_structure != expected_structure:
            reset_database()
        else:
            validate_and_fix_data(cursor)


def check_and_reset_database():
    if not os.path.exists(db_path):
        create_database()
        return
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        if get_db_structure(cursor) != expected_structure:
            reset_database()
            return
        cursor.execute("PRAGMA foreign_keys = OFF")
        for table, columns in expected_structure.items():
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            for row in rows:
                for col, dtype in columns.items():
                    value = row[list(columns.keys()).index(col)]
                    if (dtype == 'INTEGER' and not isinstance(value, int)) or \
                            (dtype == 'REAL' and not isinstance(value, float)):
                        reset_database()
                        return
        validate_and_fix_data(cursor)


def update_user_progress(G, coins, time):
    """
    Обновляет прогресс пользователя в таблице users для уровня G.

    Если в столбце `levelG_complite` (где G - номер уровня) стоит 0, то ставим 1
    и увеличиваем `total_complite` на 1. Если `total_complite` стало >= G, возвращаем True,
    иначе False.

    :param G: Номер уровня (целое число от 1 до 4)
    :return: True, если `total_complite` стало >= G, иначе False
    """
    levels = {1: 'levelOne',
              2: 'levelTwo',
              3: 'levelThree',
              4: 'levelFour'}
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'game')
    if G not in {1, 2, 3, 4}:
        raise ValueError("G должен быть от 1 до 4")
    s = {1: 'levelOne_complite',
         2: 'levelTwo_complite',
         3: 'levelThree_complite',
         4: 'levelFour_complite'}
    column_name = s[G]
    level_table_name = levels[G]
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(f"SELECT {column_name}, total_complite FROM users")
        result = cursor.fetchone()

        cursor.execute(f"SELECT time, coins FROM {level_table_name}")
        result2 = cursor.fetchone()

        if result is None:
            raise ValueError("В таблице users нет данных")
        if result2 is None:
            cursor.execute(f"INSERT INTO {level_table_name} (time, coins) VALUES ({time}, {coins})")
            conn.commit()
        else:
            time_before, coins_before = result2
            if time_before > time:
                time_before = time
            if coins_before < coins:
                coins_before = coins
            cursor.execute(f"UPDATE {level_table_name} SET time = {time_before}, coins = {coins_before}")
            conn.commit()

        level_status, total_complite = result

        if level_status == 0:
            new_total = total_complite + 1
            cursor.execute(f"UPDATE users SET {column_name} = 1, total_complite = ?",
                           (new_total,))
            conn.commit()
        else:
            new_total = total_complite

        return new_total >= G


def check_level_completion(G):
    """
    Проверяет, пройден ли уровень G в таблице users.

    :param G: Номер уровня (целое число от 1 до 4)
    :return: True, если уровень пройден (1), иначе False
    """
    s = {1: 'levelOne_complite',
         2: 'levelTwo_complite',
         3: 'levelThree_complite',
         4: 'levelFour_complite'}

    if G not in s:
        raise ValueError("G должен быть от 1 до 4")

    column_name = s[G]

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {column_name} FROM users")
        result = cursor.fetchone()

        if result is None:
            raise ValueError("В таблице users нет данных")

        return result[0] == 1


def get_level_info(G):
    s = {1: 'levelOne',
         2: 'levelTwo',
         3: 'levelThree',
         4: 'levelFour'}
    level_name = s[G]
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT time, coins FROM {level_name}")
        result = cursor.fetchone()
    return result
