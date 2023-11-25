import sqlite3


def query_from_all_db(commits, tasks, messages, crunches):
    conn = sqlite3.connect('D:/Python projects/ExperimentalProject/hahaton.db')
    cursor = conn.cursor()

    for person_id, value in commits.items():
        # --- Выборка из таблицы BurnedPeople и Persons нужна для заполнения BurnedPeople значениями словарей
        # --- используемых в нижней функции, + именами и фамилиями
        # --- можно было бы сделать запрос по-умному, но у нас руки кривые
        cursor.execute("SELECT * FROM BurnedPeople WHERE PersonId = ?", (person_id,))
        existing_record = cursor.fetchone()
        cursor.execute("SELECT Name, LastName FROM Persons WHERE Persons.ID = ?", (person_id,))
        person_info = cursor.fetchone()

        if person_info:
            name, lastname = person_info
        else:
            # --- на всякий проставляем дефолтные значения хардкодом -- мало ли случится что
            name, lastname = "Неизвестен", "Неизвестен"

        # --- Проверка на существующую запись
        # --- дабы по 100 раз не добавлять одних и тех же людей
        if existing_record:
            # Если запись существует, обновляем
            cursor.execute("""
                UPDATE BurnedPeople
                SET `Commit` = ?, Name = ?, LastName = ?
                WHERE PersonId = ?
            """, (value, name, lastname, person_id))
        else:
            # Если запись отсутствует, вставляем новую
            cursor.execute("""
                INSERT INTO BurnedPeople (PersonId, `Commit`, Name, LastName)
                VALUES (?, ?, ?, ?)
            """, (person_id, value, name, lastname))

    # --- В этих трех циклах постепенно заполняем все поля таблицы
    # --- Опять же, можно было бы сделать умнее (наверное), но как умеем
    for person_id, value in tasks.items():
        cursor.execute("UPDATE BurnedPeople SET Task = ? WHERE PersonId = ?", (value, person_id))

    for person_id, value in messages.items():
        cursor.execute("UPDATE BurnedPeople SET Message = ? WHERE PersonId = ?", (value, person_id))

    for person_id, value in crunches.items():
        cursor.execute("UPDATE BurnedPeople SET Crunch = ? WHERE PersonId = ?", (value, person_id))

    # --- СУММА проставлена на случай другого подхода к подсчету шансов
    # --- Запрос, необходимый для подсчёта шансов
    cursor.execute(
        "SELECT PersonId, SUM(`Commit`), SUM(Task), SUM(Message), SUM(Crunch) FROM BurnedPeople GROUP BY PersonId")
    result = cursor.fetchall()

    #--- Обрабатываем результат запроса
    for row in result:
        person_id, commit_sum, task_sum, message_sum, crunch_sum = row
        # --- Гипотетически КОММИТАМ, ТАСКАМ, СООБЩЕНИЯМ(упадок сообщений) и КРАНЧАМ проставляем "веса"
        # --- Эти самые "веса" будем считать способом определять, какие из событий (коммиты, кранчи и т.д.)
        # --- имеют больше важности / наиболее критичны
        # --- В данном случае нас сильно пугают кранчи, например
        burn_chance = (commit_sum*0.3 + task_sum*0.2 + message_sum * 0.2 + crunch_sum*0.35)*100
        complete_burn_chance = round(burn_chance, 1)
        cursor.execute("UPDATE BurnedPeople SET BurnChance = ? WHERE PersonId = ?", (complete_burn_chance, person_id))
        print(f"{complete_burn_chance}%")
    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


# --- Просто удобное место, чтобы прописывать итог алгоритма
# --- Передаем аргументы функции из main.py, они сюда поставляются как множества
def count_burnout_chance(*, suppose_commits, suppose_tasks, suppose_messages, suppose_crunches):
    # --- Ввиду последнего комментария, заставляем множества стать словарями
    commits = dict(sorted(suppose_commits.items()))
    tasks = dict(sorted(suppose_tasks.items()))
    messages = dict(sorted(suppose_messages.items()))
    crunches = dict(sorted(suppose_crunches.items()))

    # --- А вот и используем функцию с кучей SQL-запросов, которая висит выше
    query_from_all_db(commits, tasks, messages, crunches)

    # --- Результат функции:
    # --- 35.0%
    # --- 55.0%
    # --- 20.0%
    # --- 85.0%
    # --- 0.0%
    # --- 0.0%
    # --- 35.0%






