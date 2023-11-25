import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime


def count_messages():
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('hahaton.db')
    cursor = conn.cursor()

    # Получение информации о пользователях из таблицы Persons
    cursor.execute("SELECT ID, Name, LastName FROM Persons")
    user_info = cursor.fetchall()

    # Словарь для хранения результатов сгорания для каждого пользователя
    burnout_results = {}

    # Перебор уникальных пользователей
    for user_data in user_info:
        user_id, name, last_name = user_data
        cursor.execute(
            "SELECT Date, Amount FROM Messages WHERE PersonId = ? AND Date BETWEEN '2023-10-01' AND '2023-11-30'",
            (user_id,))
        rows = cursor.fetchall()

        # Разделение данных на даты и количество сообщений
        dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in rows]
        messages_per_day = [row[1] for row in rows]

        # Построение графика для каждого пользователя
        plt.figure(figsize=(10, 6))
        plt.plot(dates, messages_per_day, label=f'{name} {last_name}')

        # Вычисление среднего количества сообщений
        average_messages = sum(messages_per_day) / len(messages_per_day)
        average_line = [average_messages] * len(messages_per_day)
        plt.plot(dates, average_line, label='Среднее количество сообщений', linestyle='--')

        # Линия на 0.7 от среднего количества сообщений
        threshold = 0.7 * average_messages
        line_07_average = [threshold] * len(messages_per_day)
        plt.plot(dates, line_07_average, label='0.7 от среднего количества сообщений', linestyle='-.', color='red')

        # Настройка осей и меток
        plt.xlabel('Дата')
        plt.ylabel('Количество сообщений')
        plt.title(f'График сообщений для {name} {last_name}')

        # Добавление легенды
        plt.legend()

        # Отображение графика
        plt.tight_layout()
        plt.show()

        # Вычисление сгорания для пользователя
        below_threshold_count = 0
        below_threshold_days = 0
        threshold_exceeded = False

        for msg in messages_per_day:
            if msg < threshold:
                below_threshold_days += 1
                if below_threshold_days > 3 and not threshold_exceeded:
                    below_threshold_count += 1
                    threshold_exceeded = True
            else:
                below_threshold_days = 0
                threshold_exceeded = False

        # Сохранение результатов сгорания для пользователя
        burnout_results[(name, last_name)] = below_threshold_count

    # Закрытие соединения с базой данных
    conn.close()

    # Вывод результатов сгорания для всех пользователей
    for (name, last_name), count in burnout_results.items():
        print(f'{name} {last_name}: Количество раз сгораний: {count}')

count_messages()
