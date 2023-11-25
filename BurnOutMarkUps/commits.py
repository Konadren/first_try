import sqlite3
from datetime import datetime
from UsersQuery import database_query as dbq



def count_commits_for_bad_situations():
    conn = sqlite3.connect('D:/Python projects/ExperimentalProject/hahaton.db')
    cursor = conn.cursor()

    # --- dbq.commit_query и подобные хранятся в папке UsersQuery
    # --- но мы не уверены, насколько удобно и понятно будет бегать глазами в тот и в этот файл
    # --- поэтому всё, что лежит в UsersQuery, мы переменными заменили
    # --- но в algorithm.py запросы прописали по дефолту
    cursor.execute(dbq.commit_query)
    rows = cursor.fetchall()

    # --- вспомогательный словарь для плохих коммитов юзера в неделю
    bad_commit_counts_by_person_and_week = {}
    # --- Отслеживаем опасные (по нашему мнению) коммиты
    # --- в надежде, что человек не будет писать fIx sTyLe и т.п.
    burnout_commits = ('FIX', 'STYLE', 'bug fix', 'style', 'fix bug', 'BUG FIX', 'FIX BUG')

    # --- А вот здесь уже основной словарь, который
    # --- мы по итогу и возвращаем как результат функции
    potential_burnout_people_with_commits = {}
    # --- Шерстим rows (строка 12)
    for commit in rows:
        commit_id, person_id, date, message, name, last_name = commit
        # --- Ищем совпадения с опасными коммитами
        # --- Вдобавок здесь создается словарь, включающий недели
        # --- Оставили такую фичу на случай модернизации или кастомайза проекта
        for bad_commit in burnout_commits:
            if bad_commit in message:
                # --- Преобразование строки с датой в объект datetime
                commit_date = datetime.strptime(date, '%Y-%m-%d')
                # --- Получение номера недели
                week_number = commit_date.isocalendar()[1]
                # --- Создаем ключ, соответствующий PersonId и неделе
                key = (person_id, week_number)

                # --- Получаем текущее количество плохих коммитов для данного ключа
                current_bad_commit_count = bad_commit_counts_by_person_and_week.get(key, 0)

                # --- Увеличиваем счетчик ПЛОХИХ коммитов для текущей недели и PersonId
                bad_commit_counts_by_person_and_week[key] = current_bad_commit_count + 1
                # --- Увеличиваем счетчик ПЛОХИХ коммитов для текущей недели и PersonId
                if key in bad_commit_counts_by_person_and_week:
                    bad_commit_counts_by_person_and_week[key] += 1
                else:
                    bad_commit_counts_by_person_and_week[key] = 1

    # --- Важная часть функции: ищем погорельцев, у которых больше 4 коммитов за неделю (могли бы взять любое значение)
    # --- и проставляем ключом айдишник, а значением -- 1 / 0
    for (person_id, _), bad_commit_count in bad_commit_counts_by_person_and_week.items():
        if bad_commit_count > 4:
            potential_burnout_people_with_commits[person_id] = 1
        else:
            potential_burnout_people_with_commits[person_id] = 0

    return potential_burnout_people_with_commits




