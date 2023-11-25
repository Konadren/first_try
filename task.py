import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def count_tasks():
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('hahaton.db')
    cursor = conn.cursor()

    # Получение уникальных идентификаторов пользователей
    cursor.execute("SELECT DISTINCT PersonId FROM TasksChanges")
    user_ids = cursor.fetchall()

    # Начальная дата
    start_date = datetime.strptime('2023-10-01', '%Y-%m-%d')

    # Словарь для хранения результатов сгорания для каждого пользователя
    burnout_results = {}

    # Перебор уникальных пользователей
    for user_id in user_ids:
        user_id = user_id[0]  # user_id является кортежем, берем первый элемент

        # Получение всех записей о количестве тасков для пользователя за заданный период
        cursor.execute(
            "SELECT Date, Amount FROM TasksChanges WHERE PersonId = ? AND Date BETWEEN '2023-10-01' AND '2023-11-30'",
            (user_id,))
        rows = cursor.fetchall()

        # Создание словаря для хранения суммы тасков по неделям
        weekly_tasks = {}

        # Обработка записей и суммирование тасков по неделям
        for row in rows:
            date = datetime.strptime(row[0], '%Y-%m-%d')
            # Определение, в какую неделю попадает дата
            week_number = (date - start_date).days // 7 + 1
            week_start = start_date + timedelta(weeks=week_number - 1)
            week_end = start_date + timedelta(weeks=week_number) - timedelta(days=1)
            week_key = f"{week_start.strftime('%Y-%m-%d')} - {week_end.strftime('%Y-%m-%d')}"
            if week_key not in weekly_tasks:
                weekly_tasks[week_key] = 0
            weekly_tasks[week_key] += row[1]

        # Проверка на превышение 17 тасков за неделю
        for week, tasks_count in weekly_tasks.items():
            if tasks_count > 17:  # Проверка на превышение 17 тасков
                print(
                    f'У пользователя {user_id} риск выгорания в неделю {week}! Общее количество тасков: {tasks_count}')

        # Добавление результатов сгорания для пользователя в общий словарь
        burnout_results[user_id] = weekly_tasks

    # Закрытие соединения с базой данных
    conn.close()

    # Построение графиков суммы тасков по неделям для каждого пользователя
    for user_id, weekly_tasks in burnout_results.items():
        weeks = list(weekly_tasks.keys())
        tasks_count = list(weekly_tasks.values())

        plt.figure(figsize=(10, 6))
        plt.bar(weeks, tasks_count, label=f'Пользователь {user_id}')

        # Линия на уровне 17 тасков
        plt.axhline(y=17, color='red', linestyle='--', label='Уровень тасков')

        # Настройка осей и меток
        plt.xlabel('Период')
        plt.ylabel('Общее количество тасков')
        plt.title(f'График тасков для Пользователя {user_id}')

        # Поворот дат на оси X для лучшей читаемости
        plt.xticks(rotation=45, ha='right')

        # Добавление легенды
        plt.legend()

        # Отображение графика
        plt.tight_layout()
        plt.show()
