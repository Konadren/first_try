from datetime import datetime

from BurnOutMarkUps.crunches import count_crunches
from BurnOutMarkUps.messages import count_messages
from BurnOutMarkUps.task import count_tasks
from BurnOutMarkUps.commits import count_commits_for_bad_situations
from BurnOutAlgorithm import algorithm


# --- В теории заместо хардкода сюда должны передаваться
# --- значения, выбранные пользователем сайта
start_date = datetime(2023, 10, 1)
end_date = datetime(2023, 10, 31)

# --- каждый SUPPOSE возвращает словарь, необходимый для нашего решения
algorithm.count_burnout_chance(suppose_commits=count_commits_for_bad_situations(start_date, end_date),
                                suppose_tasks=count_tasks(start_date, end_date),
                                suppose_crunches=count_crunches(start_date, end_date),
                                suppose_messages=count_messages(start_date, end_date))
