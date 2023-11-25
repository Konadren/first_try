import numpy as np
import matplotlib.pyplot as plt
from crunches import count_crunches
from messages import count_messages
from task import count_tasks
from commits import bad_commit_counts_by_person_and_week

# Получаем уникальные идентификаторы пользователей
user_ids = set(user_id for user_id, _ in bad_commit_counts_by_person_and_week)

# Вычисляем количество subplot'ов в зависимости от числа уникальных PersonId
num_subplots = len(user_ids)

# Создаем subplot'ы
fig, axs = plt.subplots(1, num_subplots, figsize=(12, 6))

# Создаем графики для каждого пользователя
for idx, user_id in enumerate(user_ids):
    user_data = {key: value for key, value in bad_commit_counts_by_person_and_week.items() if key[0] == user_id}
    categories, bad_commits = zip(*user_data.items())

    axs[idx].bar(np.arange(len(categories)), bad_commits, label=f'Плохие коммиты (PersonId={user_id})')

    # Добавление заголовка и подписей к осям
    axs[idx].set_title(f'Коммиты (PersonId={user_id})')
    axs[idx].set_xlabel('Недели')
    axs[idx].set_ylabel('Кол-во')
    axs[idx].legend()

# Отображение диаграмм
# plt.tight_layout()
# plt.show()
count_tasks()
count_messages()
count_crunches()