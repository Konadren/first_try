import numpy as np
import matplotlib.pyplot as plt

# Пример данных
categories = ['01.10.23', '02.10.23', '03.10.23', '04.10.23', '05.10.23']
values_part1 = [2, 3, 1, 0, 4]
values_part2 = [10, 12, 11, 9, 8]

# Создание столбчатой диаграммы с двумя частями разных цветов
bar1 = plt.bar(np.arange(len(categories)), values_part1, color='red',  label='Плохие коммиты')
bar2 = plt.bar(categories, values_part2, color='green', label='Всего коммитов', bottom=values_part1)

for idx, value in enumerate(values_part1):
    plt.text(idx, value + values_part2[idx], str(value + values_part2[idx]), ha='center', va='bottom')


# Добавление заголовка и подписей к осям
plt.title('Коммиты')
plt.xlabel('Дни')
plt.ylabel('Кол-во')
plt.legend()

# Отображение диаграммы
plt.show()

