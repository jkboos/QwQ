import requests
import discord
from datetime import datetime

base_url = "https://api.quavergame.com/v2"
user_base_url = f"{base_url}/user"

gamemode_format = {1: "4k", 2: "7k"}

class User:
    def __init__(self, data):
        self.__name = data['username']
        self.__id = data['id']
        self.__time_registered = data['time_registered']
        self.__latest_activity = data['latest_activity']
        self.__avatar_url = data['avatar_url']
        self.__default_mode = data['misc_information']['default_mode']
        self.__stats_keys4 = data['stats_keys4']
        self.__stats_keys7 = data['stats_keys7']

    @property
    def name(self) -> str: return self.__name
    @property
    def id(self) -> int: return self.__id
    @property
    def time_registered(self) -> str: return self.__time_registered
    @property
    def latest_activity(self) -> str: return self.__latest_activity
    @property
    def avatar_url(self) -> str: return self.__avatar_url
    @property
    def default_mode(self) -> int: return self.__default_mode
    @property
    def stats_keys4(self) -> dict: return self.__stats_keys4
    @property
    def stats_keys7(self) -> dict: return self.__stats_keys7

class Record:
    def __init__(self, data):
        self.__user_id = data['user_id']
        self.__map = data['map']        
        self.__date = datetime.fromisoformat(data['timestamp'])
        self.__failed = data['failed']
        self.__total_score = data['total_score']
        self.__accuracy = data['accuracy']
        self.__max_combo =  data['max_combo']
        self.__count_marvelous = data['count_marvelous']
        self.__count_perfect = data['count_perfect']
        self.__count_great = data['count_great']
        self.__count_good = data['count_good']
        self.__count_okay = data['count_okay']
        self.__count_miss = data['count_miss']
        self.__grade = data['grade']
        self.__rate = data['performance_rating']

    
    @property
    def user_id(self) -> int: return self.__user_id
    @property
    def map(self) -> dict: return self.__map
    @property
    def date(self) -> datetime: return self.__date
    @property
    def failed(self) -> bool: return self.__failed
    @property
    def total_score(self) -> int: return self.__total_score
    @property
    def accuracy(self) -> float: return self.__accuracy
    @property
    def max_combo(self) -> int: return self.__max_combo
    @property
    def count_marvelous(self) -> int: return self.__count_marvelous
    @property
    def count_perfect(self) -> int: return self.__count_perfect
    @property
    def count_great(self) -> int: return self.__count_great
    @property
    def count_good(self) -> int: return self.__count_good
    @property
    def count_okay(self) -> int: return self.__count_okay
    @property
    def count_miss(self) -> int: return self.__count_miss
    @property
    def grade(self) -> str: return self.__grade
    @property
    def rate(self) -> float: return self.__rate

    # map thumbnail (https://cdn.quavergame.com/mapsets/<mapset_id>.jpg)
    @property
    def map_thumbnail(self) -> str: return f"https://cdn.quavergame.com/mapsets/{self.map['mapset_id']}.jpg"
    # map url (https://quavergame.com/mapset/map/<map_id>)
    @property
    def map_url(self) -> str: return f"https://quavergame.com/mapset/map/{self.map['id']}"
    @property
    def map_name(self) -> str: return self.map['title']



# Get user by id or username
def GetUser(name: str) -> User:
    # GET /user/:name
    url = f"{user_base_url}/{name}"

    response = requests.get(url=url)

    if(response.status_code == 200):
        data = response.json()
        if(data):
            return User(data['user'])
    elif(response.status_code == 429):
        raise ConnectionRefusedError("Exceed rate limit.")
        
    return

def GetRecentPlayed(id: int, mode: int) -> Record:
    url = f"{user_base_url}/{id}/scores/{mode}/recent"
    response = requests.get(url=url)

    if(response.status_code == 200):
        data = response.json()['scores']
        if(data):
            return Record(data[0])
    elif(response.status_code == 429):
        raise ConnectionRefusedError("Exceed rate limit.")
        
    return


def CreateUserEmbed(user: User) -> discord.Embed:
    embed = discord.Embed(title=user.name, url=f"https://quavergame.com/user/{user.id}", description=f"預設模式: {gamemode_format[user.default_mode]}", color=0x00f7ff)
    embed.set_thumbnail(url=user.avatar_url)

    embed.add_field(name="4K",
                    value=
                    f"Global Rank:    `{user.stats_keys4['ranks']['global']}`\n"
                    f"Country Rank:   `{user.stats_keys4['ranks']['country']}`\n\n"
                    f"Overall Rating: `{round(user.stats_keys4['overall_performance_rating'], 2)}`\n"
                    f"Accuracy:       `{round(user.stats_keys4['overall_accuracy'], 2)}%`\n"
                    f"Ranked Score:   `{user.stats_keys4['ranked_score']}`\n"
                    f"Total Score:    `{user.stats_keys4['total_score']}`\n"
                    f"Total Hits:     `{user.stats_keys4['total_marvelous']+user.stats_keys4['total_perfect']+user.stats_keys4['total_great']+user.stats_keys4['total_good']+user.stats_keys4['total_okay']}`\n"
                    f"Max Combo:      `{user.stats_keys4['max_combo']}`\n"
                    f"Play Count:     `{user.stats_keys4['play_count']}`\n",
                    inline=True)
    
    embed.add_field(name="7K",
                    value=
                    f"Global Rank:    `{user.stats_keys7['ranks']['global']}`\n"
                    f"Country Rank:   `{user.stats_keys7['ranks']['country']}`\n\n"
                    f"Overall Rating: `{round(user.stats_keys7['overall_performance_rating'], 2)}`\n"
                    f"Accuracy:       `{round(user.stats_keys7['overall_accuracy'], 2)}%`\n"
                    f"Ranked Score:   `{user.stats_keys7['ranked_score']}`\n"
                    f"Total Score:    `{user.stats_keys7['total_score']}`\n"
                    f"Total Hits:     `{user.stats_keys7['total_marvelous']+user.stats_keys7['total_perfect']+user.stats_keys7['total_great']+user.stats_keys7['total_good']+user.stats_keys7['total_okay']}`\n"
                    f"Max Combo:      `{user.stats_keys7['max_combo']}`\n"
                    f"Play Count:     `{user.stats_keys7['play_count']}`\n",
                    inline=True)
    return embed

def CreateRecordEmbed(record: Record, discord_avatar: str):
    user = GetUser(record.user_id)

    embed = discord.Embed(title=f"{record.map['artist']} - {record.map_name} [{gamemode_format[record.map['game_mode']]}]", url=record.map_url, color=(0xff0000 if(record.failed) else 0x00ff00), description=f"初始難度: {round(record.map['difficulty_rating'], 2)}")
    embed.set_image(url=record.map_thumbnail)
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_footer(text=f"{user.name} {record.date.strftime('%Y-%m-%d %H:%M:%S')}", icon_url=discord_avatar)
    embed.set_author(name=f"rating: {round(record.rate, 2)}", icon_url=f"https://static.quavergame.com/img/grades/{record.grade}.png")

    embed.add_field(name="Score", value=record.total_score, inline=True)
    embed.add_field(name="Accuracy", value=f"{round(record.accuracy, 2)}%", inline=True)
    embed.add_field(name="Combo", value=record.max_combo, inline=False)
    embed.add_field(name="Marvelous", value=record.count_marvelous, inline=True)
    embed.add_field(name="Perfect", value=record.count_perfect, inline=True)
    embed.add_field(name="Great", value=record.count_great, inline=True)
    embed.add_field(name="Good", value=record.count_good, inline=True)
    embed.add_field(name="Okay", value=record.count_okay, inline=True)
    embed.add_field(name="Miss", value=record.count_miss, inline=True)

    return embed

# print(GetUser("jkboos").id)