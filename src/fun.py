from classes import HeadHunter, SuperJob, Vacancy


def user_interaction():
    """
    Взаимодействия с пользователем
    """
    platforms = int(
        input("Выберите платформы, с которых хотите получить вакансии:\n1 - HH\n2 - SJ\n3 - обе платформы\n"))
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").lower().split()
    return platforms, search_query, top_n, filter_words


def get_list_of_vacancies(platforms: int, search_query: str):
    """
    Получает вакансии от сервера при помощи создания экземпляров классов получения данных по API
    и создает экземпляры класса Vacancies по полученным данным
    :param platforms:
    :param search_query:
    :return:
    """
    hh_api = HeadHunter()
    superjob_api = SuperJob()
    list_of_vacancis = []
    hh_vacancies = hh_api.get_vacancies(search_query)
    superjob_vacancies = superjob_api.get_vacancies(search_query)
    if platforms == 1:
        for item_id, vacancy in hh_vacancies.items():
            list_of_vacancis.append(
                Vacancy(item_id, vacancy["name"], vacancy["url"], vacancy["salary from"], vacancy["salary to"],
                        vacancy["experience"],
                        vacancy["tasks"]))  # Создание экземпляров класса для работы с вакансиями HH
    elif platforms == 2:
        for item_id, vacancy in superjob_vacancies.items():
            list_of_vacancis.append(
                Vacancy(item_id, vacancy["name"], vacancy["url"], vacancy["salary from"], vacancy["salary to"],
                        vacancy["experience"],
                        vacancy["tasks"]))  # Создание экземпляров класса для работы с вакансиями SJ
    elif platforms == 3:
        for item_id, vacancy in {**superjob_vacancies, **hh_vacancies}.items():
            list_of_vacancis.append(
                Vacancy(item_id, vacancy["name"], vacancy["url"], vacancy["salary from"], vacancy["salary to"],
                        vacancy["experience"],
                        vacancy["tasks"]))  # Создание экземпляров класса для работы с вакансиями обеих платформ

    return list_of_vacancis


def sort_and_filter_top_vac(list_of_vacancis, top_n, filter_words):
    """
    Сортирует по убыванию зарплаты и фильтрует по ключевым словам, полученным от пользователя
    :param list_of_vacancis:
    :param top_n:
    :param filter_words:
    :return:
    """
    vacs_set = set()
    for vac in list_of_vacancis:
        for word in filter_words:
            if word in vac.tasks.lower() or word in vac.name.lower():
                vacs_set.add(vac)
    if not vacs_set:
        print("Нет вакансий, соответствующих заданным критериям.")
    list_of_vacancis = sorted(list(vacs_set), key=lambda x: -float(x))
    return list_of_vacancis[:top_n]


def print_vacancies(top_vac):
    """
    Выводит в консоль краткую информацию о вакансиях
    :param top_vac:
    :return:
    """
    for item in top_vac:
        print(f"{item.name}\n{item.url}\n{float(item)}\n")
