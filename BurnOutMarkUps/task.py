import sqlite3
from datetime import datetime, timedelta
from UsersQuery import database_query as dbq


def count_tasks():
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('D:/Python projects/ExperimentalProject/hahaton.db')
    cursor = conn.cursor()

    # Получение уникальных идентификаторов пользователей
    cursor.execute(dbq.tasks_query_1)
    user_ids = cursor.fetchall()

    # Начальная дата ВСТАВИТЬ СЮДА ИНПУТ ПОЛЬЗОВАТЕЛЯ С САЙТА
    start_date = datetime.strptime('2023-10-01', '%Y-%m-%d')

    # Словарь для хранения результатов сгорания для каждого пользователя
    burnout_results = {}

    over_tasks_for_human = {}

    # Перебор уникальных пользователей
    for user_tuple in user_ids:
        user_id = user_tuple[0]  # user_id является первым элементом кортежа


        # Получение всех записей о количестве тасков для пользователя за заданный период
        cursor.execute(
            "SELECT Date, Amount FROM TasksChanges WHERE PersonId = ? AND Date BETWEEN '2023-10-01' AND '2023-11-30'",
            (user_id,))
        # print(f"Rows for user {user_id}: {cursor.fetchall()}")
        rows = cursor.fetchall()


        # Создание словаря для хранения суммы тасков по неделям и айдишника работника
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

       # print(weekly_tasks.items())
        # --- проверка на превышение 17 тасков за неделю
        # --- где 17 тасок -- предполагаемое ГРАНИЧНОЕ значение для
        # --- большой нагрузки на человека

        for week, tasks_count in weekly_tasks.items():
            if tasks_count > 17:
                # Если user_id уже есть в словаре, увеличиваем значение на 1
                # Если user_id отсутствует, добавляем его в словарь со значением 1
                over_tasks_for_human[user_id] = 1
                # print(
                #     f'У пользователя {user_id} риск выгорания в неделю {week}! Общее количество тасков: {tasks_count}')
            else:
                over_tasks_for_human[user_id] = 0

        # Добавление результатов сгорания для пользователя в общий словарь
        burnout_results[user_id] = weekly_tasks

    # Закрытие соединения с базой данных должно быть за пределами цикла for
    conn.close()
    return over_tasks_for_human
