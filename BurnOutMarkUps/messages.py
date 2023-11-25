import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
from UsersQuery import database_query as dbq


def count_messages():
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('D:/Python projects/ExperimentalProject/hahaton.db')
    cursor = conn.cursor()

    # Получение информации о пользователях из таблицы Persons
    cursor.execute("SELECT * FROM Persons")
    user_info = cursor.fetchall()

    # Словарь для хранения результатов сгорания для каждого пользователя
    burnout_results = {}




    # Перебор уникальных пользователей
    for user_data in user_info:
        user_id, name, last_name = user_data
        cursor.execute(dbq.messages_query,
            (user_id,))
        rows = cursor.fetchall()

        # Разделение данных на даты и количество сообщений
        dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in rows]
        messages_per_day = [row[1] for row in rows]
        # Вычисление среднего количества сообщений
        if messages_per_day:
            average_messages = sum(messages_per_day) / len(messages_per_day)
        else:
            average_messages = 0

        average_line = [average_messages] * len(messages_per_day)
        # burn_out_edge = average_messages

        # Вычисление сгорания для пользователя
        below_threshold_count = 0
        below_threshold_days = 0
        burn_out_edge_exceeded = False

        for msg in messages_per_day:
            if msg < average_messages*0.7:
                below_threshold_days += 1
                if below_threshold_days > 3 and not burn_out_edge_exceeded:
                    below_threshold_count += 1
                    burn_out_edge_exceeded = True
            else:
                below_threshold_days = 0
                burn_out_edge_exceeded = False

        # Сохранение результатов сгорания для пользователя
        burnout_results[user_id] = below_threshold_count

    # Закрытие соединения с базой данных
    conn.close()

    # Вывод результатов сгорания для всех пользователей
    # for (name, last_name), count in burnout_results.items():
    #     print(f'{name} {last_name}: Количество раз сгораний: {count}')
    return burnout_results
