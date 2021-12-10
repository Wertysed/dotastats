import requests
import discord
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix=settings['prefix'])
bot.remove_command('help')


class DotaAPI:
    BASE_URL: str = 'https://api.opendota.com/api/'

    @classmethod
    def record_search(cls, id_of_player, name_of_discipline: str, name_of_hero: str):
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

    @classmethod
    def stats_with_peers(cls, id_of_player):
        url = f'{cls.BASE_URL}players/{id_of_player}/peers'
        abobus = requests.get(url).json()
        return cls.information_output(abobus, 1)

    @classmethod
    def stats_of_word(cls, id_of_player, name_of_hero):
        url = f'{cls.BASE_URL}players/{id_of_player}/wordcloud'
        abobus = requests.get(url).json()
        if name_of_hero == 'all':
            print(abobus)
            return cls.information_output(abobus, 2)
        else:
            id_of_hero = cls.search_id_of_hero(name_of_hero)
            url_new = f'{url}?hero_id={id_of_hero}'
            abobus_new = requests.get(url_new).json()
            print(abobus_new)
            return cls.information_output(abobus_new, 2)

    @classmethod
    def stats_of_team(cls, name_of_team):
        id_of_team = cls.search_id_of_team(name_of_team)
        url = f'{cls.BASE_URL}teams/{id_of_team}'
        abobus = requests.get(url).json()
        return cls.information_output(abobus, 2)

    @classmethod
    def stats_of_all_team_players(cls, name_of_team):
        id_of_team = cls.search_id_of_team(name_of_team)
        url = f'{cls.BASE_URL}teams/{id_of_team}/players'
        abobus = requests.get(url).json()
        for i in abobus:
            if i['is_current_team_member']:
                for key, value in i.items():
                    print(key, ':', value)

    @classmethod
    def stats_of_all_team_hero(cls, name_of_team, name_of_hero):
        id_of_team = cls.search_id_of_team(name_of_team)
        id_of_hero = cls.search_id_of_hero(name_of_hero)
        url = f'{cls.BASE_URL}teams/{id_of_team}/heroes'
        abobus = requests.get(url).json()
        for i in abobus:
            if i['hero_id'] == id_of_hero:
                cls.information_output(i, 2)


@bot.command()
async def st_for_pl(ctx, argument):
    argument = int(argument)
    await ctx.send(DotaAPI.stats_of_player(argument))


@bot.command()
async def record(ctx, argument_1, argument_2, *, argument_3):
    argument_1 = int(argument_1)
    argument_2 = str(argument_2)
    await ctx.send(DotaAPI.record_search(argument_1, argument_2, argument_3))


@bot.command()
async def wl(ctx, argument_1, *, argument_2):
    argument_1 = int(argument_1)
    await ctx.send(DotaAPI.wl_of_player(argument_1, argument_2))

@bot.command()
async def friends(ctx, argument):
    argument = int(argument)
    await ctx.send(DotaAPI.stats_with_peers(argument))

@bot.command()
async def wordcloud(ctx, argument_1, *, argument_2):
    argument_1 = int(argument_1)
    await ctx.send(DotaAPI.stats_of_word(argument_1, argument_2))

@bot.command()
async def team(ctx, *, argument):
    await ctx.send(DotaAPI.stats_of_team(argument))

@bot.command()
async def team_player(ctx, *, argument):
    await ctx.send(DotaAPI.stats_of_all_team_players(argument))

@bot.command()
async def team_hero(ctx, argument_1, *, argument_2):
    argument_1 = argument_1.replace('_', ' ')
    await ctx.send(DotaAPI.stats_of_all_team_hero(argument_1 , argument_2))


bot.run(settings['token'])






# print('пример рекорда', DotaAPI.record_search(339665220, 'kills', 'all'))  # внешний функционал
# print('пример поиска id команды по названию', DotaAPI.search_id_of_team('PSG.LGD'))  # внутренний функционал
# print('пример получения id по названию героя', DotaAPI.search_id_of_hero('Slark'))  # внутренний функционал
# print('пример получения статы игрока', DotaAPI.stats_of_player(339665220))  # внешний функционал
# print('пример получения статы побед и поражений', DotaAPI.wl_of_player(339665220, 'Slark'))  # внешний функционал
# print('пример статы с друзьями', DotaAPI.stats_with_peers(1084744980))  # внешний функционал
# print('пример вывода ласт слов', DotaAPI.stats_of_word(1084744980, 'Luna'))  # внешний функционал
# print('пример получения статы про команд', DotaAPI.stats_of_team('Team Spirit'))  # внешний функционал
# print('пример получения статы для каждого игорка(играющего)', DotaAPI.stats_of_all_team_players('PSG.LGD'))  #
# внешний функционал
# print('пример получения статы с определнным героем', DotaAPI.stats_of_all_team_hero('Team Spirit', 'Magnus'))  #
# внешний функционал
