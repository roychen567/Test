import re
from os import environ

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
SESSION = environ.get('SESSION', 'Media_searcher')
API_ID = int(environ.get('API_ID', '21881785'))
API_HASH = environ.get('API_HASH', '3ea846a3df1b63221ddc0ae02df04a43')
BOT_TOKEN = environ.get('BOT_TOKEN', '1786837074:AAGpLvsYWB7oENdg_3KZ8WfFYxfs77w5RMU')

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = True 
PICS = (environ.get('PICS' ,'https://graph.org/file/9c023dd906352100948c8.mp4')).split()

# Admins, Channels & Users
OWNER_ID = environ.get('OWNER_ID', '1380904444')
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '1380904444').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1002203759750').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_grp = environ.get('AUTH_GROUP')
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# MongoDB information
DATABASE_NAME = environ.get('DATABASE_NAME', "Roy")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'andi')
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://Roy:Roy@alanwalker1.bv4gl.mongodb.net/?retryWrites=true&w=majority&appName=Alanwalker1")
DATABASE_URI2 = environ.get('DATABASE_URI2', "mongodb+srv://Roy:Roy@alanwalker2.x9yrb.mongodb.net/?retryWrites=true&w=majority&appName=Alanwalker2")
DATABASE_URI3 = environ.get('DATABASE_URI3', "mongodb+srv://roychen8900:roychen8900@testing3.xx84xv7.mongodb.net/?retryWrites=true&w=majority&appName=Testing3")

# FSUB
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
# Set to False inside the bracket if you don't want to use Request Channel else set it to Channel ID
REQ_CHANNEL1=environ.get("REQ_CHANNEL1", None)
REQ_CHANNEL1 = (int(REQ_CHANNEL1) if REQ_CHANNEL1 and id_pattern.search(REQ_CHANNEL1) else False) if REQ_CHANNEL1 is not None else None
REQ_CHANNEL2 = environ.get("REQ_CHANNEL2", None)
REQ_CHANNEL2 = (int(REQ_CHANNEL2) if REQ_CHANNEL2 and id_pattern.search(REQ_CHANNEL2) else False) if REQ_CHANNEL2 is not None else None
JOIN_REQS_DB = environ.get("JOIN_REQS_DB", DATABASE_URI)
DELETE_TIMEOUT = int(environ.get('DELETE_TIMEOUT', 2*60*60)) # 2 hours in seconds

# Others
AUTO_DEL = int(300)
PM_DEL = int(300)

LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002289384769'))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', '+MxeWYzJmeGgyNmU1')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "True")), True)
IMDB = is_enabled((environ.get('IMDB', "False")), False)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<b>{file_name}</b>\n\n🔘 size - {file_size}")
BATCH_FILE_CAPTION = CUSTOM_FILE_CAPTION
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>Query: {query}</b> \n‌‌‌‌IMDb Data:\n\n🏷 Title: <a href={url}>{title}</a>\n🎭 Genres: {genres}\n📆 Year: <a href={url}/releaseinfo>{year}</a>\n🌟 Rating: <a href={url}/ratings>{rating}</a> / 10")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "False")), False)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)

LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"
