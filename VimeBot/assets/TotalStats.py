import requests, json

def TotalStats():
    _TotalStats = {"kills": 0, "deaths": 0, "wins": 0, "games": 0}
    users = json.loads(requests.get("https://api.vimeworld.ru/leaderboard/get/arc/wins?size=1000").text)["records"]

    for user in users:
        for item in _TotalStats:
            _TotalStats[item] += user[item]

    return _TotalStats, len(users)