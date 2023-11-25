import sqlite3
from datetime import datetime, timedelta
from UsersQuery import database_query as dbq
from UsersPreferedDates.dates import start_date


def count_tasks():
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('D:/Python projects/ExperimentalProject/hahaton.db')
    cursor = conn.cursor()

    # Получение уникальных идентификаторов пользователей
    cursor.execute(dbq.tasks_query_1)
    user_ids = cursor.fetchall()

    over_tasks_for_human = {}

    # Перебор уникальных пользователей
    for user_tuple in user_ids:
        user_id = user_tuple[0]  # user_id является первым элементом кортежа

        # Получение всех записей о количестве тасков для пользователя за заданный период
        cursor.execute(
            dbq.tasks_query_2,
            (user_id,))
        rows = cursor.fetchall()

        # Создание словаря для хранения суммы тасков по неделям и айдишника работника
        weekly_tasks = {}

        # --- Ищем таски, сортируем их по неделям
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

        # --- проверка на превышение 17 тасков за неделю
        # --- где 17 тасок -- предполагаемое ГРАНИЧНОЕ значение для
        # --- большой нагрузки на человека
        for week, tasks_count in weekly_tasks.items():
            if tasks_count > 17:
                # --- По тенденции уже проставляем 1, если человек в зоне риска
                # --- и 0, если нет
                over_tasks_for_human[user_id] = 1
            else:
                over_tasks_for_human[user_id] = 0

    conn.close()
    return over_tasks_for_human
