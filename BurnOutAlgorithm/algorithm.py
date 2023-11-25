import sqlite3

def count_burnout_chance(*, suppose_commits, suppose_tasks, suppose_messages, suppose_crunches):


    commits = dict(sorted(suppose_commits.items()))
    tasks = dict(sorted(suppose_tasks.items()))
    messages = dict(sorted(suppose_messages.items()))
    crunches = dict(sorted(suppose_crunches.items()))

    print(commits)
    print(tasks)
    print(messages)
    print(crunches)

    conn = sqlite3.connect('D:/Python projects/ExperimentalProject/hahaton.db')
    cursor = conn.cursor()

    # for person_id, value in commits.items():
    #     cursor.execute("INSERT INTO BurnedPeople (PersonId, `Commit`)"
    #                    "VALUES (?, ?)", (person_id, value))

    for person_id, value in tasks.items():
        cursor.execute("UPDATE BurnedPeople SET Task = ? WHERE PersonId = ?", (value, person_id))

    for person_id, value in messages.items():
        cursor.execute("UPDATE BurnedPeople SET Message = ? WHERE PersonId = ?", (value, person_id))

    for person_id, value in crunches.items():
        cursor.execute("UPDATE BurnedPeople SET Crunch = ? WHERE PersonId = ?", (value, person_id))


    # Сохранение изменений и закрытие соединения
    conn.commit()

