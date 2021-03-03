import requests, json


with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

DEFAULT_SESSION = "https://api.vimeworld.ru"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36', 'accept': '*/*'}
TOKEN = "?token=" + config["vime_token"]


def ConnectionApi():
    return "https://api.vimeworld.ru"


'''
Возвращает информацию об игроке или нескольких игроках по их нику. 
Если игрок не найден, то он не будет показываться в ответе.
'''


def GetPlayersName(names, session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/user/name/" + names + token, headers=headers)
    return response.text


'''
Возвращает информацию об игроке или нескольких игроках по их id. 
Если игрок с заданым id не найден, то он не будет показан в ответе.
'''


def GetPlayersId(ids, session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/user/" + ids + token, headers=headers)
    return response.text


'''
Возвращает список друзей игрока.
'''


def GetPlayerFriends(id, session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/user/" + id + "/friends" + token, headers=headers)
    return response.text


'''
Возвращает статус игрока онлайн, человекопонятное сообщение и название 
игры, где он находится.
'''


def GetPlayersSession(id, session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/user/" + id + "/session" + token, headers=headers)
    return response.text


'''
Возвращает статистику всех игр, в которые играл запрашиваемый игрок.
'''


def GetPlayerStats(id, games=None, session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    if games is None:
        response = requests.get(session + "/user/" + id + "/stats" + token, headers=headers)
    else:
        response = requests.get(session + "/user/" + id + "/stats" + "?" + games + token, headers=headers)

    return response.text


'''
Возвращает список всех достижений игрока. 
'''
"""
Метод может вернуть id достижений, которых нет в списке всех достижений. 
Это секретные достижения, их id находится в промежутке от 9000 до 9100.
"""


def GetPlayerAchievements(id, session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/user/" + id + "/achievements" + token, headers=headers)
    return response.text


'''
Возвращает список таблиц рекордов, куда попал данный игрок, и место в них. 
'''


def GetPlayerLeaderboards(id, session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/user/" + id + "/leaderboards" + token, headers=headers)
    return response.text


'''
Получает последние матчи игрока
'''


def GetPlayerMatches(id, session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/user/" + id + "/matches" + token, headers=headers)
    return response.text


'''
Массовое получение статуса (до 50)
'''


def GetSession(ids, session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/user/session/" + ids + token, headers=headers)
    return response.text


'''
Очень массовое получение статуса (до 1000)
'''
"""
Возвращает статус игроков онлайн, человекопонятное сообщение и название игры, 
где каждый из них находится.

В теле POST запроса должен быть JSON массив с айдишниками игроков. Например, 
для получения статуса игроков 134568 и 94245, тело запроса должно быть следующим:

[134568,94245]
"""


def GetSessions(ids, session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/user/session" + ids + token, headers=headers)
    return response.text


'''
Ищет гильдии по названию или тегу
'''
"""
Возвращает список гильдий, название или тег которых содержит заданный запрос. 
Максимальное количество гильдий в ответе 10. При сортировке гильдий в ответе 
учитывается полное совпадение по тегу/названию, уровень и еще пару хитрых штук.

Параметры
query - запрос для поиска (минимум 2 символа)
"""


def SearchGuild(query, session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/guild/search?query=" + query + token, headers=headers)
    return response.text


'''
Получает информацию о гильдии
'''
"""
Искать гильдию можно по её id, названию или тегу. Для этого нужно указать один из 
следующих параметров.

Параметры
id* - Получение по id гильдии.
name* - Получение по названию гильдии.
tag* - Получение по тегу гильдии.
"""


def GetGuild(arg, data, session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/guild/get?" + arg +"="+ data + token, headers=headers)
    return response.text


'''
Список таблиц рекордов
'''
"""
Ответ
type - Тип таблицы рекордов, он используется для получения конкретной таблицы рекордов в методе leaderboard/get.
description - Краткое описание таблицы рекордов.
sort - Список доступных вариантов таблицы рекордов.
"""


def ListLeaderboard(session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/leaderboard/list" + token, headers=headers)
    return response.text


# Тут должен быть этот метод: /leaderboard/get/:type[/:sort] 


'''
Количество игроков онлайн
'''
"""
Возвращает количество игроков онлайн. В сумме и по каждой игре отдельно.

Ответ
total - Общий онлайн на MiniGames.
separated - Онлайн отдельно по каждой мини игре.
"""


def Online(session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/online" + token, headers=headers)
    return response.text


'''
Список стримов, которые в данный момент идут на сервере
'''
"""
Возвращает список активных стримов на сервере. Этот список идентичен тому, 
что показывается на сервере MiniGames в меню по команде /streams.

Ответ
title - Заголовок стрима. Может содержать символы юникода.
owner - Ник ютубера, который добавил (ведет) стрим.
viewers - Количество зрителей стрима.
duration - Длительность стрима в секундах (время с начала стрима).
platform - Платформа, на которой идет стрим
"""


def OnlineStreams(session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/online/streams" + token, headers=headers)
    return response.text


'''
Список модераторов онлайн
'''


def OnlineStaff(session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/online/staff" + token, headers=headers)
    return response.text


'''
Полная информация о матче
'''


def GetMatch(id, session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/match/" + id + token, headers=headers)
    return response.text


'''
Человекочитаемые названия игр, статистики, рангов
'''


def GetLocale(session=DEFAULT_SESSION, name="ru", token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/locale/" + name + token, headers=headers)
    return response.text


'''
Список игр, по которым ведется статистика
'''


def GetMiscGames(session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/misc/games" + token, headers=headers)
    return response.text


'''
Список карт, сгруппированный по играм
'''


def GetMiscMaps(session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/misc/maps" + token, headers=headers)
    return response.text


'''
Список всех возможных достижений
'''


def GetMiscAchievements(session=DEFAULT_SESSION, token=TOKEN, headers=HEADERS):
    response = requests.get(session + "/misc/achievements" + token, headers=headers)
    return response.text


def GetSkin(id, session="http://skin.vimeworld.ru/raw/skin/playboi_.png?_="):
    p = requests.get(session+id)
    out = open("assets/TemporaryPictures/img.jpg", "wb")
    out.write(p.content)
    out.close()


if __name__ == "__main__":
    pass
