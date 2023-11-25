import sqlite3
from datetime import datetime
from UsersQuery import database_query as dbq

# Функция для подсчета работы более 222 часов за месяц
def count_crunches(start_date, end_date):
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('hahaton.db')
    cursor = conn.cursor()

    # Получение информации о пользователях и их идентификаторах из таблицы work_hours
    cursor.execute(dbq.crunches_query_1)
    user_info = cursor.fetchall()

    # Словарь для хранения информации о превышении часов работы для каждого пользователя
    exceeded_hours = {}

    # Перебор уникальных пользователей
    for user_data in user_info:
        user_id, name, last_name = user_data

        # Получение всех записей о времени работы для пользователя за заданный период
        cursor.execute(dbq.crunches_query_2, (user_id,))
        rows = cursor.fetchall()

        # Обработка записей и накопление часов работы за месяц
        total_hours_worked = 0
        for row in rows:
            date = datetime.strptime(row[0], '%Y-%m-%d')

            # Проверка, попадает ли дата в заданный интервал
            if start_date <= date <= end_date:
                total_hours_worked += row[1]

        # Проверка на превышение 222 часов и запись метки (1 или 0) в словарь
        if total_hours_worked > 50:
            exceeded_hours[user_id] = 1
        else:
            exceeded_hours[user_id] = 0

    # Закрытие соединения с базой данных
    conn.close()
    return exceeded_hours


