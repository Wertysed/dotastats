import requests
from collections.abc import Iterator
import json

url = 'https://api.opendota.com/api/teams'
url_2 = 'https://api.opendota.com/api/matches/6310996743'
url_3 = 'https://api.opendota.com/api/players/1084744980/wl'
url_4 = 'https://api.opendota.com/api/heroes'
url_5 = 'https://api.opendota.com/api/heroes/11/itemPopularity'
url_6 = 'https://api.opendota.com/api/teams/'

url_8 = 'https://api.opendota.com/api/players/186807667/recentMatches'
class Player:
    pass


# for i in c:
#    print(i)


def search_id_of_team(zxc):
    abobus = requests.get(url).json()
    value = 0
    for i in abobus:
        if zxc == abobus[value]['name']:
            return abobus[value]['team_id']
        value += 1


def search_id_of_hero(zxc):
    abobus_of_heros = requests.get(url_4).json()
    value = 0
    for i in abobus_of_heros:
        if zxc == i['localized_name']:
            return i['id']
        value += 1


b = search_id_of_hero('Ember Spirit')
print(search_id_of_hero('Lycan'))

abobus = requests.get(url_2).json()
# print(abobus)

abobus_player = requests.get(url_5).json()
#print('dd', abobus_player)

print(abobus_player)
c = search_id_of_team('Team Spirit')
url_7 = f'{url_6}{c}/heroes'
print(url_7)
abobus_team = requests.get(url_8).json()
print(abobus_team)
#for i in abobus_player:
#    for key, value in i.items():
#        print(key, ":", value)
for i in abobus_team:
    for key, value in i.items():
        print(key, ":", value)


for key, value in abobus_player.items():
    print(key)
    for key_1, value_2 in value.items():
        print(key_1, ":", value_2)
    print('fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')


for key, value in abobus_team.items(): # выводить статистику игры
    print(key, ":", value)

