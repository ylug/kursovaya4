from classes import JsonSave
from fun import user_interaction, get_list_of_vacancies, sort_and_filter_top_vac, print_vacancies

if __name__ == "__main__":
    user_input = user_interaction()
    list_of_vac = get_list_of_vacancies(user_input[0], user_input[1])
    json_file = JsonSave(user_input[1])
    json_file.save_to_file(list_of_vac)

    top_vac = sort_and_filter_top_vac(list_of_vac, user_input[2], user_input[3])
    print_vacancies(top_vac)
