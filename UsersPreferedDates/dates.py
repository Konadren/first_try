
import sqlite3
from datetime import datetime


def parse_dates_db():
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('D:/Python projects/ExperimentalProject/hahaton.db')
    cursor = conn.cursor()

    # Получение последней записи из таблицы main_date
    cursor.execute("SELECT start_date, end_date FROM main_date ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()  # Получаем данные

    if data:
        start_date_not_completed, end_date_not_completed = data
    else:
        print("Записи в таблице не найдены")

    # Закрытие соединения с базой данных
    conn.close()

    return start_date_not_completed, end_date_not_completed


start_date_not_completed, end_date_not_completed = parse_dates_db()

year1 = int(start_date_not_completed[0:4])
month1 = int(start_date_not_completed[5:7])
day1 = int(start_date_not_completed[8:10])

year2 = int(end_date_not_completed[0:4])
month2 = int(end_date_not_completed[5:7])
day2 = int(end_date_not_completed[8:10])

start_date = datetime(year1, month1, day1)
end_date = datetime(year2, month2, day2)





