from datetime import datetime

from BurnOutMarkUps.crunches import count_crunches
from BurnOutMarkUps.messages import count_messages
from BurnOutMarkUps.task import count_tasks
from BurnOutMarkUps.commits import count_commits_for_bad_situations
from BurnOutAlgorithm import algorithm
from UsersPreferedDates.dates import start_date, end_date


# --- каждый SUPPOSE возвращает словарь, необходимый для нашего решения
algorithm.count_burnout_chance(suppose_commits=count_commits_for_bad_situations(),
                                suppose_tasks=count_tasks(),
                                suppose_crunches=count_crunches(start_date, end_date),
                                suppose_messages=count_messages())
