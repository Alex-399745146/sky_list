# main.py
"""Модуль основной логики"""
from src.api_clients import APIAdapter

# Создание экземпляра класса для работы с API сайтов с самолетами
api = APIAdapter()

# Получение информации о самолетах с opensky-network.org
aeroplanes = api.get_aeroplanes('Spain')

# Преобразование набора данных в список объектов
aeroplanes = Aeroplane.cast_to_object_list(aeroplanes)

# Пример работы контструктора класса с одним самолетом
aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)

# Сохранение информации в файл
json_saver = JSONSaver()
json_saver.add_aeroplane(vacancy)
json_saver.delete_aeroplane(vacancy)


# Функция для взаимодействия с пользователем
def user_interaction():
    country = input("Введите название страны: ")
    top_n = int(input("Введите количество самолетов для вывода в топ N: "))
    filter_words = input("Введите названия стран для фильтрации по стране регистрации: ").split()
    altitude_range = input("Введите диапазон высот полета: ") # Пример: 100000 - 150000

    filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)

    ranged_aeroplanes = get_aeroplanes_by_altitude(aeroplanes, altitude_range)

    sorted_aeroplanes = sort_aeroplanes(ranged_aeroplanes)
    top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)
    print_aeroplanes(top_aeroplanes)


if __name__ == "__main__":
    # user_interaction()  # точка входа в прогу
    pass
