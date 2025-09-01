# (c) adarsh-goel (c) @biisal
import os, re
from os import getenv, environ
from dotenv import load_dotenv



load_dotenv()
bot_name = "file to link bot"
bisal_channel = "https://telegram.me/bisal_files"
bisal_grp = "https://t.me/+PA8OPL2Zglk3MDM1"

class Var(object):
    MULTI_CLIENT = False 
    BLACKLIST_WORDS = (
    list(os.environ.get("BLACKLIST_WORDS").split(","))
    if os.environ.get("BLACKLIST_WORDS")
    else []
    )

    BLACKLIST_WORDS = ["www 1TamilMV nexus", "www 1TamilMV mov", "www 1TamiMV kids", "AML", "telugu_moviez", "[CC]", "[CF]", "TeamCinepleX", "www 7MovieRulz mn", "www 1TamilMV vin", "www 1TamilMV cafe", "@ADrama  Lovers", "www 1TamilMV help", "KC", "@CK Moviez", "E4E", "[BindasMovies]", "[Hezz Movies]", "www Tamilblasters rent", "[CH]", "www 4MovieRulz com", "www TamilBlasters cam", "www Tamilblasters social", "[@The 4x Team]", "@mj link 4u", "[CD]", "@Andhra movies", "@BT MOVIES HD", "Telegram@APDBackup", "Telegram@Alpacinodump", "www 1TamilMV fans", "@Ruraljat Studio", "7HitMovies bio", "[MZM]", "[@UCMOVIE]", "@CC_New", "[MF]", "@Mallu_Movies", "[MC]", "[@MociesVerse]", "@Mm_Linkz", "@BT_MOVIES_HD_@FILMSCLUB04", "www TamilVaathi online", "www 1TamilMV mx", "@BGM LinkzZ", "www 1TamilMV media", "[D&O]", "[MM]", "[", "]", "[FC]", "[CF]", "LinkZz", "[DFBC]", "@New_Movie", "@Infinite_Movies2", "MM", "@R A R B G", "[F&T]", "[KMH]", "[DnO]", "[F&T]", "MLM", "@TM_LMO", "@x265_E4E", "@HEVC MoviesZ", "SSDMovies", "@MM Linkz", "[CC]", "@Mallu_Movies", "@DK Drama", "@luxmv_Linkz", "@Akw_links", "CK HEVC", "@Team_HDT", "[CP]", "www 1TamilMV men", "www TamilRockers", "@MM", "@mm", "[MW]", "@TN68 Linkzz", "@Clipmate_Movie", "[MASHOBUC]", "Official TheMoviesBoss", "www CineVez one", "www 7MovieRulz lv", "www 1TamilMV vip", "[SMM Official]", "[Movie Bazar]", "@BM_Links", "[CG]", "Filmy4wap xyz", "www 1TamilMV pw", "www TamilBlasters pm", "[FH]", "Torrent911 tv", "[MZM]", "www CineVez top", "www CineVez top", "www 7MovieRulz sx", "[YDF]", "www 1TamilMV art", "www TamilBlasters me", "[mwkOTT]", "@Tamil_LinkzZ", "[LV]", "@The_4x_Team", "TheMoviesBoss"]

    API_ID = int(getenv('API_ID', '22301351'))
    API_HASH = str(getenv('API_HASH', '3035f2bbd92a9c5174d174d92b52b25b'))
    BOT_TOKEN = str(getenv('BOT_TOKEN' , '8231344175:AAFQFqx9RtqW3A2t4EE4oaIfylKjfaddr4M'))
    name = str(getenv('name', '@Testadm789bot'))
    SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
    WORKERS = int(getenv('WORKERS', '4'))
    BIN_CHANNEL = int(getenv('BIN_CHANNEL', '-1002108978238'))
    NEW_USER_LOG = int(getenv('NEW_USER_LOG', '-1002108978238'))
    PORT = int(getenv('PORT', '8080'))
    BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
    PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
    OWNER_ID = [int(x) for x in os.environ.get("OWNER_ID", "5721673207").split()]
    NO_PORT = bool(getenv('NO_PORT', False))
    APP_NAME = None
    OWNER_USERNAME = str(getenv('OWNER_USERNAME', 'AkshayChand08'))
    if 'DYNO' in environ:
        ON_HEROKU = True
        APP_NAME = str(getenv('APP_NAME')) #dont need to fill anything here
    
    else:
        ON_HEROKU = False
    FQDN = str(getenv('FQDN', 'BIND_ADRESS:PORT')) if not ON_HEROKU or getenv('FQDN', '') else APP_NAME+'.herokuapp.com'
    HAS_SSL=bool(getenv('HAS_SSL',True))
    if HAS_SSL:
        URL = "https://{}/".format(FQDN)
    else:
        URL = "https://{}/".format(FQDN)
    FQDN = "https://a-s-disk.koyeb.app/"
    DATABASE_URL = str(getenv('DATABASE_URL', 'mongodb+srv://iPapcorn:iPapcorn@cluster0.52lnvxn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'))
    UPDATES_CHANNEL = str(getenv('UPDATES_CHANNEL', None)) 
    BANNED_CHANNELS = list(set(int(x) for x in str(getenv("BANNED_CHANNELS", "")).split()))   
    BAN_CHNL = list(set(int(x) for x in str(getenv("BAN_CHNL", "")).split()))   
    BAN_ALERT = str(getenv('BAN_ALERT' , '<b>ʏᴏᴜʀ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ.Pʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ @biisal_bot ᴛᴏ ʀᴇsᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇ!!</b>'))




def replace_username(text):
    prohibitedWords = Var.BLACKLIST_WORDS
    big_regex = re.compile('|'.join(map(re.escape, prohibitedWords)))
    text = big_regex.sub("", text)

    usernames = re.findall("([@][A-Za-z0-9_]+)", text)
    for i in usernames:
        text = text.replace(i, "")

    return text

