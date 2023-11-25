import sqlite3
from datetime import datetime, timedelta


def count_crunches():
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('hahaton.db')
    cursor = conn.cursor()

    # Получение информации о пользователях и их идентификаторах из таблицы work_hours
    cursor.execute("SELECT DISTINCT work_hours.PersonId, Persons.Name, Persons.LastName FROM work_hours JOIN Persons "
                   "ON work_hours.PersonId = Persons.ID")
    user_info = cursor.fetchall()

    # Словарь для хранения информации о превышении часов работы для каждой недели каждого пользователя
    exceeded_hours = {}

    # Перебор уникальных пользователей
    for user_data in user_info:
        user_id, name, last_name = user_data

        # Получение всех записей о времени работы для пользователя за заданный период
        cursor.execute(
            "SELECT Date, Hours_worked FROM work_hours WHERE PersonId = ? AND Date BETWEEN '2023-10-01' AND "
            "'2023-11-30'",
            (user_id,))
        rows = cursor.fetchall()

        # Обработка записей и накопление часов работы по неделям
        for row in rows:
            date = datetime.strptime(row[0], '%Y-%m-%d')
            week_start = date - timedelta(days=date.weekday())  # Начало недели (понедельник)

            # Получение номера недели в году
            week_number = date.isocalendar()[1]

            # Получение ключа для недели данного пользователя
            week_key = f"{date.year}_{week_number}"

            # Инициализация информации о превышении часов для данного пользователя и недели
            if week_key not in exceeded_hours:
                exceeded_hours[week_key] = {user_id: 0}
            elif user_id not in exceeded_hours[week_key]:
                exceeded_hours[week_key][user_id] = 0

            # Накопление часов работы для данного пользователя и недели
            exceeded_hours[week_key][user_id] += row[1]

    # Проверка на превышение 25 часов и вывод предупреждения, если это первое превышение за неделю
    for week_data in exceeded_hours.items():
        for user_id, hours_worked in week_data[1].items():
            if hours_worked > 25:
                week_start = datetime.strptime(week_data[0] + '-1', "%Y_%W-%w")
                week_end = week_start + timedelta(days=6)
                print(
                    f'У работника {name} {last_name} (PersonId: {user_id}) риск переработки в неделю с {week_start.strftime("%Y-%m-%d")} по {week_end.strftime("%Y-%m-%d")}! Общее время переработки: {hours_worked} часов')

    # Закрытие соединения с базой данных
    conn.close()

count_crunches()
