import requests
from collections.abc import Iterator
import json

url = 'https://api.opendota.com/api/players/1084744980'
url_2 = 'https://api.opendota.com/api/matches/6310996743'
url_3 = 'https://api.opendota.com/api/players/6313647601/wordcloud?hero_id=84'
url_4 = 'https://api.opendota.com/api/heroes'
url_5 = 'https://api.opendota.com/api/heroes/11/itemPopularity'
url_6 = 'https://api.opendota.com/api/teams/'

url_8 = 'https://api.opendota.com/api/players/998767228/matches'




class DotaAPI:
    BASE_URL: str = 'https://api.opendota.com/api/'

    @classmethod
    def record_search(cls, id_of_player, name_of_discipline: str, name_of_hero):
        max_discipline = 0
        url = f'{cls.BASE_URL}players/{id_of_player}/matches'
        matches = requests.get(url).json()
        if name_of_hero == 'all':
            for i in matches:
                if max_discipline < i[name_of_discipline]:
                    max_discipline = i[name_of_discipline]
            return f'максимум {name_of_discipline} - {max_discipline}'
        else:
            id_of_hero = cls.search_id_of_hero(name_of_hero)
            url_new = f'{url}?hero_id={id_of_hero}'
            matches_on_hero = requests.get(url_new).json()
            for i in matches_on_hero:
                if max_discipline < i[name_of_discipline]:
                    max_discipline = i[name_of_discipline]
            return f'максимум {name_of_discipline} - {max_discipline}'

    @classmethod
    def search_id_of_team(cls, name_of_team: str):
        url = f'{cls.BASE_URL}teams'
        abobus = requests.get(url).json()
        value = 0
        for i in abobus:
            if name_of_team == abobus[value]['name']:
                return abobus[value]['team_id']
            value += 1

    @classmethod
    def search_id_of_hero(cls, name_of_hero):
        url = f'{cls.BASE_URL}heroes'
        abobus_of_heros = requests.get(url).json()
        for i in abobus_of_heros:
            if name_of_hero == i['localized_name']:
                return i['id']

    @classmethod
    def information_output(cls, request_api, way):
        if way == 1:  # словарь в списке
            for i in request_api:
                for key, value in i.items():
                    print(key, ":", value)
        elif way == 2:  # словарь
            for key, value in request_api.items():
                if isinstance(value, dict):
                    print(key)
                    for key_1, value_2 in value.items():
                        print(key_1, ":", value_2)
                else:
                    print(key, ':', value)
        elif way == 3:
            for key, value in request_api.items():  # не нужен, наверное
                print(key, ":", value)

    @classmethod
    def stats_of_player(cls, id_of_player):
        url = f'{cls.BASE_URL}players/{id_of_player}'
        abobus = requests.get(url).json()
        return cls.information_output(abobus, 2)

    @classmethod
    def wl_of_player(cls, id_of_player: int, name_of_hero: str):
        url = f'{cls.BASE_URL}players/{id_of_player}/wl'
        abobus = requests.get(url).json()
        if name_of_hero == 'all':
            return cls.information_output(abobus, 2)
        else:
            id_of_hero = cls.search_id_of_hero(name_of_hero)
            url_new = f'{url}?hero_id={id_of_hero}'
            abobus_new = requests.get(url_new).json()
            return cls.information_output(abobus_new, 2)




print('пример рекорда', DotaAPI.record_search(339665220, 'kills', 'all'))
print('пример поиска id команды по названию', DotaAPI.search_id_of_team('PSG.LGD'))
print('пример получения id по названию героя', DotaAPI.search_id_of_hero('Slark'))
print('пример получения статы игрока', DotaAPI.stats_of_player(339665220))
print('пример получения статы побед и поражений', DotaAPI.wl_of_player(339665220, 'Slark'))
