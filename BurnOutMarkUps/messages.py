
import sqlite3
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
        cursor.execute(dbq.messages_query, (user_id,))
        rows = cursor.fetchall()

        messages_per_day = [row[1] for row in rows]
        # Вычисление среднего количества сообщений
        if messages_per_day:
            average_messages = sum(messages_per_day) / len(messages_per_day)
        else:
            average_messages = 0

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

        # --- Самая важная часть функции
        burnout_results[user_id] = below_threshold_count
        
    conn.close()
    # Закрытие соединения с базой данных
    return burnout_results
