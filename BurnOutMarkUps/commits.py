import sqlite3
from datetime import datetime
from UsersQuery import database_query as dbq
conn = sqlite3.connect('D:/Python projects/ExperimentalProject/hahaton.db')
cursor = conn.cursor()

cursor.execute(dbq.commit_query)
rows = cursor.fetchall()

# Словарь для хранения счетчика ПЛОХИХ коммитов для каждого PersonId и недели
bad_commit_counts_by_person_and_week = {}

burnout_commits = ('FIX', 'STYLE', 'bug fix', 'style', 'fix bug', 'BUG FIX', 'FIX BUG')

potential_burnout_people_with_commits = set()  # Используем множество для уникальных значений PersonId


def count_commits_for_bad_situations():
    for commit in rows:
        commit_id, person_id, date, message, name, last_name = commit
        # print(f"Commit ID: {commit_id}, Person ID: {person_id}, Date: {date}, Message: {message}, Name: {name}, Last "
        #       f"Name: {last_name}")

        for bad_commit in burnout_commits:
            if bad_commit in message:
                # Преобразование строки с датой в объект datetime
                commit_date = datetime.strptime(date, '%Y-%m-%d')
                # Получение номера недели
                week_number = commit_date.isocalendar()[1]
                # Создаем ключ, соответствующий PersonId и неделе
                key = (person_id, week_number)

                # Получаем текущее количество плохих коммитов для данного ключа
                current_bad_commit_count = bad_commit_counts_by_person_and_week.get(key, 0)

                # Увеличиваем счетчик ПЛОХИХ коммитов для текущей недели и PersonId
                bad_commit_counts_by_person_and_week[key] = current_bad_commit_count + 1
                # Увеличиваем счетчик ПЛОХИХ коммитов для текущей недели и PersonId
                if key in bad_commit_counts_by_person_and_week:
                    bad_commit_counts_by_person_and_week[key] += 1

                else:
                    bad_commit_counts_by_person_and_week[key] = 1

    # Поиск потенциальных "погорельцев" с более чем 3 плохими коммитами
    for (person_id, _), bad_commit_count in bad_commit_counts_by_person_and_week.items():
        if bad_commit_count > 3:
            potential_burnout_people_with_commits.add(person_id)

    # print(f'Потенциальные погорельцы {potential_burnout_people_with_commits}')

    # Вывод количества плохих коммитов для каждой недели и PersonId
    # for (person_id, week_number), bad_commit_count in bad_commit_counts_by_person_and_week.items():
    #     print(
    #         f"Week: {week_number}, Person ID: {person_id}, Bad Commits: {bad_commit_count}")

    # счетчик ПЛОХИХ коммитов
    # print("Total Bad Commits:", sum(bad_commit_counts_by_person_and_week.values()))
    # print(bad_commit_counts_by_person_and_week)
    conn.close()

    return potential_burnout_people_with_commits




