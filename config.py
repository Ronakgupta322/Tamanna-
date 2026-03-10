import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()


def get_int_env(name: str, default=None, required: bool = False) -> int:
    value = getenv(name)
    if value is None or value == "":
        if required:
            raise SystemExit(f"[ERROR] - Required environment variable missing: {name}")
        return default
    try:
        return int(value)
    except ValueError:
        raise SystemExit(f"[ERROR] - {name} must be an integer.")


def get_str_env(name: str, default=None, required: bool = False) -> str:
    value = getenv(name, default)
    if required and (value is None or value == ""):
        raise SystemExit(f"[ERROR] - Required environment variable missing: {name}")
    return value


API_ID = get_int_env("API_ID", required=True)
API_HASH = get_str_env("API_HASH", required=True)

YTPROXY_URL = get_str_env("YTPROXY_URL", "https://tgapi.xbitcode.com")
YT_API_KEY = get_str_env("YT_API_KEY", "xbit_M79PCh3BWqCHuXxDagWV5jfNrZBKjd7p")
BOT_TOKEN = get_str_env("BOT_TOKEN", required=True)

OWNER_USERNAME = get_str_env("OWNER_USERNAME", "")
BOT_USERNAME = get_str_env("BOT_USERNAME", "")
BOT_NAME = get_str_env("BOT_NAME", "")
ASSUSERNAME = get_str_env("ASSUSERNAME", "")
MONGO_DB_URI = get_str_env("MONGO_DB_URI", None)

DURATION_LIMIT_MIN = get_int_env("DURATION_LIMIT", 17000)
LOGGER_ID = get_int_env("LOG_GROUP_ID", required=True)
OWNER_ID = get_int_env("OWNER_ID", required=True)

HEROKU_APP_NAME = get_str_env("HEROKU_APP_NAME")
HEROKU_API_KEY = get_str_env("HEROKU_API_KEY")

UPSTREAM_REPO = get_str_env("UPSTREAM_REPO", "https://github.com/Ronakgupta322/Tamanna-")
UPSTREAM_BRANCH = get_str_env("UPSTREAM_BRANCH", "main")
GIT_TOKEN = get_str_env("GIT_TOKEN", None)

PRIVACY_LINK = get_str_env(
    "PRIVACY_LINK",
    "https://telegra.ph/Privacy-Policy-for-RishuMusic-01-09-2",
)
SUPPORT_CHANNEL = get_str_env("SUPPORT_CHANNEL", "https://t.me/UFC_UPDATES")
SUPPORT_CHAT = get_str_env("SUPPORT_CHAT", "https://t.me/UFC_UPDATES")

AUTO_LEAVING_ASSISTANT = get_str_env("AUTO_LEAVING_ASSISTANT", "True").lower() == "true"
AUTO_LEAVE_ASSISTANT_TIME = get_int_env("ASSISTANT_LEAVE_TIME", 9000)

SONG_DOWNLOAD_DURATION = get_int_env("SONG_DOWNLOAD_DURATION", 9999999)
SONG_DOWNLOAD_DURATION_LIMIT = get_int_env("SONG_DOWNLOAD_DURATION_LIMIT", 9999999)

SPOTIFY_CLIENT_ID = get_str_env("SPOTIFY_CLIENT_ID", "1c21247d714244ddbb09925dac565aed")
SPOTIFY_CLIENT_SECRET = get_str_env("SPOTIFY_CLIENT_SECRET", "709e1a2969664491b58200860623ef19")

PLAYLIST_FETCH_LIMIT = get_int_env("PLAYLIST_FETCH_LIMIT", 25)
TG_AUDIO_FILESIZE_LIMIT = get_int_env("TG_AUDIO_FILESIZE_LIMIT", 5242880000)
TG_VIDEO_FILESIZE_LIMIT = get_int_env("TG_VIDEO_FILESIZE_LIMIT", 5242880000)

STRING1 = get_str_env("STRING_SESSION", None)
STRING2 = get_str_env("STRING_SESSION2", None)
STRING3 = get_str_env("STRING_SESSION3", None)
STRING4 = get_str_env("STRING_SESSION4", None)
STRING5 = get_str_env("STRING_SESSION5", None)
STRING6 = get_str_env("STRING_SESSION6", None)
STRING7 = get_str_env("STRING_SESSION7", None)

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = get_str_env("START_IMG_URL", "https://files.catbox.moe/kol1pd.jpg")
PING_IMG_URL = get_str_env("PING_IMG_URL", "https://files.catbox.moe/xddya7.jpg")
PLAYLIST_IMG_URL = "https://files.catbox.moe/4aoc5g.jpg"
STATS_IMG_URL = "https://files.catbox.moe/kol1pd.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/kol1pd.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/kol1pd.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/kol1pd.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/kol1pd.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/kol1pd.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/kol1pd.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/kol1pd.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/kol1pd.jpg"


def time_to_seconds(time_value):
    stringt = str(time_value)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")

if SUPPORT_CHANNEL and not re.match(r"^(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit(
        "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
    )

if SUPPORT_CHAT and not re.match(r"^(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit(
        "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
    )
