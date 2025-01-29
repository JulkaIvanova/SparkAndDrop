# import os
# import sqlite3
#
# db_path = os.path.join(os.path.dirname(__file__), 'data', 'game.db')
# expected_structure = {
#     'users': {'levels_complite': 'INTEGER'},
#     'levelOne': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelTwo': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelThree': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelFour': {'time': 'REAL', 'coins': 'INTEGER'}
# }
#
# def get_db_structure(cursor):
#     structure = {}
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
#     tables = [row[0] for row in cursor.fetchall()]
#     for table in tables:
#         cursor.execute(f"PRAGMA table_info({table})")
#         structure[table] = {row[1]: row[2] for row in cursor.fetchall()}
#     return structure
#
# def create_database():
#     os.makedirs(os.path.dirname(db_path), exist_ok=True)
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         for table, columns in expected_structure.items():
#             columns_str = ', '.join(f'{col} {dtype}' for col, dtype in columns.items())
#             cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns_str})")
#         conn.commit()
#
# def reset_database():
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         for table in expected_structure.keys():
#             cursor.execute(f"DROP TABLE IF EXISTS {table}")
#         create_database()
#
# def check_and_update_database():
#     if not os.path.exists(db_path):
#         create_database()
#         return
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         current_structure = get_db_structure(cursor)
#         for table, expected_columns in expected_structure.items():
#             if table not in current_structure or current_structure[table] != expected_columns:
#                 reset_database()
#                 break
#
# check_and_update_database()


# import os
# import sqlite3
#
# db_path = os.path.join(os.path.dirname(__file__), 'data', 'game')
# expected_structure = {
#     'users': {'levels_complite': 'INTEGER DEFAULT 0'},
#     'levelOne': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelTwo': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelThree': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelFour': {'time': 'REAL', 'coins': 'INTEGER'}
# }
#
# def get_db_structure(cursor):
#     structure = {}
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
#     tables = [row[0] for row in cursor.fetchall()]
#     for table in tables:
#         cursor.execute(f"PRAGMA table_info({table})")
#         structure[table] = {row[1]: row[2] for row in cursor.fetchall()}
#     return structure
#
# def create_database():
#     os.makedirs(os.path.dirname(db_path), exist_ok=True)
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         for table, columns in expected_structure.items():
#             columns_str = ', '.join(f'{col} {dtype}' for col, dtype in columns.items())
#             cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns_str})")
#         conn.commit()
#
# def reset_database():
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         for table in expected_structure.keys():
#             cursor.execute(f"DROP TABLE IF EXISTS {table}")
#         create_database()
#
# def check_and_update_database():
#     if not os.path.exists(db_path):
#         create_database()
#         return
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         current_structure = get_db_structure(cursor)
#         for table, expected_columns in expected_structure.items():
#             if table not in current_structure or current_structure[table] != expected_columns:
#                 reset_database()
#                 break
#
# check_and_update_database()


# import os
# import sqlite3
#
# db_path = os.path.join(os.path.dirname(__file__), 'data', 'game')
# expected_structure = {
#     'users': {'levels_complite': 'INTEGER DEFAULT 0'},
#     'levelOne': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelTwo': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelThree': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelFour': {'time': 'REAL', 'coins': 'INTEGER'}
# }
#
# def get_db_structure(cursor):
#     structure = {}
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
#     tables = [row[0] for row in cursor.fetchall()]
#     for table in tables:
#         cursor.execute(f"PRAGMA table_info({table})")
#         structure[table] = {row[1]: row[2] for row in cursor.fetchall()}
#     return structure
#
# def create_database():
#     os.makedirs(os.path.dirname(db_path), exist_ok=True)
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         for table, columns in expected_structure.items():
#             columns_str = ', '.join(f'{col} {dtype}' for col, dtype in columns.items())
#             cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns_str})")
#         conn.commit()
#
# def reset_database():
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         existing_tables = get_db_structure(cursor).keys()
#         for table in existing_tables:
#             if table not in expected_structure:
#                 cursor.execute(f"DROP TABLE IF EXISTS {table}")
#         for table, expected_columns in expected_structure.items():
#             if table not in existing_tables or get_db_structure(cursor).get(table) != expected_columns:
#                 cursor.execute(f"DROP TABLE IF EXISTS {table}")
#         create_database()
#
# def check_and_update_database():
#     if not os.path.exists(db_path):
#         create_database()
#         return
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         current_structure = get_db_structure(cursor)
#         for table, expected_columns in expected_structure.items():
#             if table not in current_structure or current_structure[table] != expected_columns:
#                 reset_database()
#                 break
#
# check_and_update_database()



# import os
# import sqlite3
#
# db_path = os.path.join(os.path.dirname(__file__), 'data', 'game')
# expected_structure = {
#     'users': {'levels_complite': 'INTEGER'},
#     'levelOne': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelTwo': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelThree': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelFour': {'time': 'REAL', 'coins': 'INTEGER'}
# }
#
# def get_db_structure(cursor):
#     structure = {}
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
#     tables = [row[0] for row in cursor.fetchall()]
#     for table in tables:
#         cursor.execute(f"PRAGMA table_info({table})")
#         structure[table] = {row[1]: row[2] for row in cursor.fetchall()}
#     return structure
#
# def create_database():
#     os.makedirs(os.path.dirname(db_path), exist_ok=True)
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         for table, columns in expected_structure.items():
#             columns_str = ', '.join(f'{col} {dtype}' for col, dtype in columns.items())
#             cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns_str})")
#         cursor.execute("INSERT INTO users (levels_complite) VALUES (0)")
#         conn.commit()
#
# def reset_database():
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         existing_tables = get_db_structure(cursor).keys()
#         for table in existing_tables:
#             if table not in expected_structure:
#                 cursor.execute(f"DROP TABLE IF EXISTS {table}")
#         for table, expected_columns in expected_structure.items():
#             if table not in existing_tables or get_db_structure(cursor).get(table) != expected_columns:
#                 cursor.execute(f"DROP TABLE IF EXISTS {table}")
#         create_database()
#
# def check_and_update_database():
#     if not os.path.exists(db_path):
#         create_database()
#         return
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         current_structure = get_db_structure(cursor)
#         for table, expected_columns in expected_structure.items():
#             if table not in current_structure or current_structure[table] != expected_columns:
#                 reset_database()
#                 break
#
# check_and_update_database()


# import os
# import sqlite3
#
# db_path = os.path.join(os.path.dirname(__file__), 'data', 'game')
# expected_structure = {
#     'users': {'levels_complite': 'INTEGER'},
#     'levelOne': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelTwo': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelThree': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelFour': {'time': 'REAL', 'coins': 'INTEGER'}
# }
#
# def get_db_structure(cursor):
#     structure = {}
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
#     tables = [row[0] for row in cursor.fetchall()]
#     for table in tables:
#         cursor.execute(f"PRAGMA table_info({table})")
#         structure[table] = {row[1]: row[2] for row in cursor.fetchall()}
#     return structure
#
# def validate_and_fix_data(cursor):
#     for table, columns in expected_structure.items():
#         cursor.execute(f"SELECT * FROM {table}")
#         rows = cursor.fetchall()
#         for row in rows:
#             update_needed = False
#             update_values = {}
#             for col, dtype in columns.items():
#                 value = row[list(columns.keys()).index(col)]
#                 if dtype == 'INTEGER' and not isinstance(value, int):
#                     update_values[col] = 0
#                 elif dtype == 'REAL' and not isinstance(value, float):
#                     update_values[col] = 0.0
#             if update_values:
#                 update_needed = True
#                 set_clause = ', '.join(f"{col} = ?" for col in update_values.keys())
#                 cursor.execute(f"UPDATE {table} SET {set_clause} WHERE rowid = ?", list(update_values.values()) + [row[0]])
#         if table == 'users' and not rows:
#             cursor.execute("INSERT INTO users (levels_complite) VALUES (0)")
#
# def create_database():
#     os.makedirs(os.path.dirname(db_path), exist_ok=True)
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         for table, columns in expected_structure.items():
#             columns_str = ', '.join(f'{col} {dtype}' for col, dtype in columns.items())
#             cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns_str})")
#         cursor.execute("INSERT INTO users (levels_complite) VALUES (0)")
#         conn.commit()
#
# def reset_database():
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         existing_tables = get_db_structure(cursor).keys()
#         for table in existing_tables:
#             if table not in expected_structure:
#                 cursor.execute(f"DROP TABLE IF EXISTS {table}")
#         for table, expected_columns in expected_structure.items():
#             if table not in existing_tables or get_db_structure(cursor).get(table) != expected_columns:
#                 cursor.execute(f"DROP TABLE IF EXISTS {table}")
#         create_database()
#
# def check_and_update_database():
#     if not os.path.exists(db_path):
#         create_database()
#         return
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         current_structure = get_db_structure(cursor)
#         for table, expected_columns in expected_structure.items():
#             if table not in current_structure or current_structure[table] != expected_columns:
#                 reset_database()
#                 break
#         validate_and_fix_data(cursor)
#         conn.commit()
#
# def check_and_reset_database():
#     if not os.path.exists(db_path):
#         create_database()
#         return
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         current_structure = get_db_structure(cursor)
#         for table, expected_columns in expected_structure.items():
#             if table not in current_structure or current_structure[table] != expected_columns:
#                 reset_database()
#                 return
#         for table, columns in expected_structure.items():
#             cursor.execute(f"SELECT * FROM {table}")
#             rows = cursor.fetchall()
#             for row in rows:
#                 for col, dtype in columns.items():
#                     value = row[list(columns.keys()).index(col)]
#                     if (dtype == 'INTEGER' and not isinstance(value, int)) or \
#                        (dtype == 'REAL' and not isinstance(value, float)):
#                         reset_database()
#                         return
#         validate_and_fix_data(cursor)
#         conn.commit()
#
# check_and_update_database()

# лучшая версия пока что.!!!
#
# import os
# import sqlite3
#
# db_path = os.path.join(os.path.dirname(__file__), 'data', 'game')
# expected_structure = {
#     'users': {'levels_complite': 'INTEGER'},
#     'levelOne': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelTwo': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelThree': {'time': 'REAL', 'coins': 'INTEGER'},
#     'levelFour': {'time': 'REAL', 'coins': 'INTEGER'}
# }
#
# def get_db_structure(cursor):
#     structure = {}
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
#     tables = [row[0] for row in cursor.fetchall()]
#     for table in tables:
#         cursor.execute(f"PRAGMA table_info({table})")
#         structure[table] = {row[1]: row[2] for row in cursor.fetchall()}
#     return structure
#
# def validate_and_fix_data(cursor):
#     for table, columns in expected_structure.items():
#         cursor.execute(f"SELECT * FROM {table}")
#         rows = cursor.fetchall()
#         for row in rows:
#             update_values = {}
#             for col, dtype in columns.items():
#                 value = row[list(columns.keys()).index(col)]
#                 if dtype == 'INTEGER' and not isinstance(value, int):
#                     update_values[col] = 0
#                 elif dtype == 'REAL' and not isinstance(value, float):
#                     update_values[col] = 0.0
#             if update_values:
#                 set_clause = ', '.join(f"{col} = ?" for col in update_values.keys())
#                 cursor.execute(f"UPDATE {table} SET {set_clause} WHERE rowid = ?", list(update_values.values()) + [row[0]])
#         if table == 'users' and not rows:
#             cursor.execute("INSERT INTO users (levels_complite) VALUES (0)")
#     cursor.connection.commit()
#
# def create_database():
#     os.makedirs(os.path.dirname(db_path), exist_ok=True)
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         for table, columns in expected_structure.items():
#             columns_str = ', '.join(f'{col} {dtype}' for col, dtype in columns.items())
#             cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns_str})")
#         cursor.execute("INSERT INTO users (levels_complite) VALUES (0)")
#         conn.commit()
#
# def reset_database():
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         cursor.execute("PRAGMA foreign_keys = OFF")
#         for table in get_db_structure(cursor).keys():
#             cursor.execute(f"DROP TABLE IF EXISTS {table}")
#         create_database()
#
# def check_and_update_database():
#     if not os.path.exists(db_path):
#         create_database()
#         return
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         current_structure = get_db_structure(cursor)
#         if current_structure != expected_structure:
#             reset_database()
#         else:
#             validate_and_fix_data(cursor)
#
# def check_and_reset_database():
#     if not os.path.exists(db_path):
#         create_database()
#         return
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         if get_db_structure(cursor) != expected_structure:
#             reset_database()
#             return
#         cursor.execute("PRAGMA foreign_keys = OFF")
#         for table, columns in expected_structure.items():
#             cursor.execute(f"SELECT * FROM {table}")
#             rows = cursor.fetchall()
#             for row in rows:
#                 for col, dtype in columns.items():
#                     value = row[list(columns.keys()).index(col)]
#                     if (dtype == 'INTEGER' and not isinstance(value, int)) or \
#                        (dtype == 'REAL' and not isinstance(value, float)):
#                         reset_database()
#                         return
#         validate_and_fix_data(cursor)
#
# check_and_update_database()
#
#
#
# import sqlite3
# import os
#
# # Путь к базе данных
# db_path = os.path.join('data', 'game')
#
# # Соединение с базой данных
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()
#
# # Получаем список таблиц
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = cursor.fetchall()
#
# # Для каждой таблицы выводим её структуру
# for table in tables:
#     table_name = table[0]
#     print(f"Структура таблицы {table_name}:")
#     cursor.execute(f"PRAGMA table_info({table_name});")
#     columns = cursor.fetchall()
#     for column in columns:
#         print(column)
#     print()
#
# # Закрываем соединение
# conn.close()
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

        # Если таблица users пуста, добавляем запись по умолчанию
        if table == 'users' and not rows:
            cursor.execute(
                "INSERT INTO users (levelOne_complite, levelTwo_complite, levelThree_complite, levelFour_complite, total_complite) VALUES (0, 0, 0, 0, 0)")

    # Обновляем столбец total_complite
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
            "INSERT INTO users (levelOne_complite, levelTwo_complite, levelThree_complite, levelFour_complite, total_complite) VALUES (0, 0, 0, 0, 0)")
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


def update_user_progress(G):
    """
    Обновляет прогресс пользователя в таблице users для уровня G.

    Если в столбце `levelG_complite` (где G - номер уровня) стоит 0, то ставим 1
    и увеличиваем `total_complite` на 1. Если `total_complite` стало >= G, возвращаем True,
    иначе False.

    :param G: Номер уровня (целое число от 1 до 4)
    :return: True, если `total_complite` стало >= G, иначе False
    """
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'game')
    if G not in {1, 2, 3, 4}:  # Проверяем, что G в допустимых пределах
        raise ValueError("G должен быть от 1 до 4")
    s = {1: 'levelOne_complite',
         2: 'levelTwo_complite',
         3: 'levelThree_complite',
         4: 'levelFour_complite'}
    column_name = s[G]  # Определяем название столбца

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Получаем текущее значение уровня и общей суммы
        cursor.execute(f"SELECT {column_name}, total_complite FROM users")
        result = cursor.fetchone()
        print('res', result)

        if result is None:
            raise ValueError("В таблице users нет данных")

        level_status, total_complite = result

        if level_status == 0:
            # Если уровень ещё не пройден, обновляем его и увеличиваем total_complite
            new_total = total_complite + 1
            cursor.execute(f"UPDATE users SET {column_name} = 1, total_complite = ?",
                           (new_total,))

            conn.commit()
        else:
            new_total = total_complite  # Если уровень уже был пройден, total_complite не меняется

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

# check_and_update_database()