import sqlite3


def query_from_all_db(commits, tasks, messages, crunches):

    conn = sqlite3.connect('D:/Python projects/ExperimentalProject/hahaton.db')
    cursor = conn.cursor()

    for person_id, value in commits.items():
        cursor.execute("SELECT * FROM BurnedPeople WHERE PersonId = ?", (person_id,))
        existing_record = cursor.fetchone()
        if existing_record:
            # Если запись существует, обновляем
            cursor.execute("UPDATE BurnedPeople SET `Commit` = ? WHERE PersonId = ?", (value, person_id))
        else:
            # Если запись отсутствует, вставляем новую
            cursor.execute("INSERT INTO BurnedPeople (PersonId, `Commit`) VALUES (?, ?)", (person_id, value))

    for person_id, value in tasks.items():
        cursor.execute("UPDATE BurnedPeople SET Task = ? WHERE PersonId = ?", (value, person_id))

    for person_id, value in messages.items():
        cursor.execute("UPDATE BurnedPeople SET Message = ? WHERE PersonId = ?", (value, person_id))

    for person_id, value in crunches.items():
        cursor.execute("UPDATE BurnedPeople SET Crunch = ? WHERE PersonId = ?", (value, person_id))

    cursor.execute(
        "SELECT PersonId, SUM(`Commit`), SUM(Task), SUM(Message), SUM(Crunch) FROM BurnedPeople GROUP BY PersonId")
    result = cursor.fetchall()

    # Вывод результатов или обработка данных
    for row in result:
        person_id, commit_sum, task_sum, message_sum, crunch_sum = row
        burn_chance = (commit_sum*0.3 + task_sum*0.2 + message_sum * 0.2 + crunch_sum*0.35)*100
        complete_burn_chance = round(burn_chance, 1)
        cursor.execute("UPDATE BurnedPeople SET BurnChance = ? WHERE PersonId = ?", (complete_burn_chance, person_id))
        print(f"{complete_burn_chance}%")
    # Сохранение изменений и закрытие соединения
    conn.commit()


def count_burnout_chance(*, suppose_commits, suppose_tasks, suppose_messages, suppose_crunches):
    commits = dict(sorted(suppose_commits.items()))
    tasks = dict(sorted(suppose_tasks.items()))
    messages = dict(sorted(suppose_messages.items()))
    crunches = dict(sorted(suppose_crunches.items()))

    query_from_all_db(commits, tasks, messages, crunches)




