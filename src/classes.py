from abc import ABC, abstractmethod
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()


class Compound(ABC):

    @abstractmethod
    def __init__(self, vac_url: str):
        self.vac_url = vac_url

    @abstractmethod
    def get_vacancies(self, keyword: str):
        pass


class Save(ABC):

    @abstractmethod
    def __init__(self, file_name):
        self.file_name = file_name

    def save_fil(self):
        pass


class HeadHunter(Compound):
    """
    Получает ключевое слово и делает запрос по API на площадку.
    """

    def __init__(self):
        self.vac_url = "https://api.hh.ru/vacancies/"

    def get_vacancies(self, keyword: str):
        params = {
            "text": keyword,
            "per_page": 20,
        }
        response_hh = requests.get(self.vac_url, params=params)
        ids_hh = [item["id"] for item in response_hh.json()["items"]]
        dict_vacancies = {}
        for item_id in ids_hh:
            get_vac = requests.get(f"{self.vac_url}{item_id}").json()
            if get_vac["salary"] is None:
                salary_from = None
                salary_to = None
            else:
                salary_from = get_vac["salary"]["from"]
                salary_to = get_vac["salary"]["to"]
            dict_vacancies[item_id] = {"name": get_vac["name"], "salary from": salary_from,
                                       "salary to": salary_to, "url": get_vac["alternate_url"],
                                       "experience": get_vac["experience"]['name'], "tasks": get_vac["description"]}
        return dict_vacancies


class SuperJob(Compound):

    def __init__(self):
        self.vac_url = "https://api.superjob.ru/2.0/vacancies/"

    def get_vacancies(self, keyword: str):
        params = {
            "keyword": keyword,
            "count": 20,
        }
        headers = {
            "X-Api-App-Id": os.getenv("SJ_API_KEY"),
            "Authorization": os.getenv("Authorization"),
            "Content-Type": os.getenv("Content-Type"),
        }
        response_sj = requests.get(self.vac_url, params=params, headers=headers)
        ids_sj = [item["id"] for item in response_sj.json()["objects"]]
        dict_vacancies = {}
        for item_id in ids_sj:
            get_vac = requests.get(f"{self.vac_url}{item_id}", headers=headers).json()
            dict_vacancies[item_id] = {"name": get_vac["profession"], "salary from": get_vac["payment_from"],
                                       "salary to": get_vac["payment_to"], "url": get_vac["link"],
                                       "experience": get_vac["experience"]["title"],
                                       "tasks": get_vac["vacancyRichText"]}
        return dict_vacancies


class Vacancy:

    def __init__(self, id_vac: int, name: str, url: str, salary_from: int, salary_to: int, experience: str, tasks: str):
        try:
            self.id_vac = id_vac
            self.name = name
            self.url = url
            self.salary_from = salary_from
            self.salary_to = salary_to
            self.experience = experience
            self.tasks = tasks
        except IndexError:
            self.name = None
            self.url = None
            self.salary_from = None
            self.salary_to = None
            self.experience = None
            self.tasks = None

    def __float__(self):
        self.salary_to = None if not self.salary_to else self.salary_to
        self.salary_from = None if not self.salary_from else self.salary_from
        if self.salary_from is not None and self.salary_to is not None:
            return float((self.salary_from + self.salary_to) / 2)
        elif self.salary_from is not None and self.salary_to is None:
            return float(self.salary_from)
        elif self.salary_from is None and self.salary_to is not None:
            return float(self.salary_to)
        else:
            return 0.0

    def __ge__(self, other):
        if isinstance(other, Vacancy):
            return float(self) >= float(other)
        elif isinstance(other, int):
            return float(self) >= other
        else:
            raise ValueError("Несравниваемые объекты")

    def __le__(self, other):
        if isinstance(other, Vacancy):
            return float(self) <= float(other)
        elif isinstance(other, int):
            return float(self) <= other
        else:
            raise ValueError("Несравниваемые объекты")

    def to_dict(self):
        return {'name': self.name, "url": self.url, "salary": self.__float__(),
                "experience": self.experience, "tasks": self.tasks}


class JsonSave(Save):
    """Создает файл с ключевым словом вакансии"""

    def __init__(self, file_name):
        self.file_name = file_name

    def save_to_file(self, list_of_vacancies):
        list_of_dicts = [vac.to_dict() for vac in list_of_vacancies]
        try:
            content = json.loads(f"{self.file_name}.json")
        except json.decoder.JSONDecodeError:
            content = []
        content += list_of_dicts
        with open(f"{self.file_name}.json", "a",) as outfile:
            json.dump(list_of_dicts, outfile)
            print("Запись в файл прошла успешно")