from os import environ as env
from dotenv import load_dotenv

load_dotenv()

class Telegram:
    API_ID = int(env.get("API_ID", '23897874'))
    API_HASH = str(env.get("API_HASH", 'ec91dd01da9693911a6ee4af5d0bef2c'))
    BOT_TOKEN = str(env.get("BOT_TOKEN", '6732118607:AAGfaeeuhnClufKzn_3yxhGhNyvwgAaZ3xY'))
    OWNER_ID = int(env.get('OWNER_ID', '1881720028'))
    WORKERS = int(env.get("WORKERS", "6"))  # 6 workers = 6 commands at once
    DATABASE_URL = str(env.get('DATABASE_URL', 'mongodb+srv://sibuna123:sibuna123@personalproject.rb8q7.mongodb.net'))
    UPDATES_CHANNEL = str(env.get('UPDATES_CHANNEL', "Max_Leech_Zone_Update"))
    SESSION_NAME = str(env.get('SESSION_NAME', 'FileStream'))
    FORCE_SUB_ID = env.get('FORCE_SUB_ID', '-1001747244117')
    FORCE_SUB = env.get('FORCE_UPDATES_CHANNEL', False)
    FORCE_SUB = True if str(FORCE_SUB).lower() == "true" else False
    SLEEP_THRESHOLD = int(env.get("SLEEP_THRESHOLD", "60"))
    FILE_PIC = env.get('FILE_PIC', "https://envs.sh/nEV.jpg")
    START_PIC = env.get('START_PIC', "https://envs.sh/nQw.jpg")
    VERIFY_PIC = env.get('VERIFY_PIC', "https://graph.org/file/736e21cc0efa4d8c2a0e4.jpg")
    MULTI_CLIENT = False
    FLOG_CHANNEL = int(env.get("FLOG_CHANNEL", '-1001747244117'))   # Logs channel for file logs
    ULOG_CHANNEL = int(env.get("ULOG_CHANNEL", '-1001747244117'))   # Logs channel for user logs
    #FLOG_CHANNEL = int(env.get("FLOG_CHANNEL", '-1002373955828'))   # Logs channel for file logs
    #ULOG_CHANNEL = int(env.get("ULOG_CHANNEL", '-1002373955828'))   # Logs channel for user logs    
    MODE = env.get("MODE", "primary")
    SECONDARY = True if MODE.lower() == "secondary" else False
    AUTH_USERS = list(set(int(x) for x in str(env.get("AUTH_USERS", "1881720028 5301275567")).split()))    
    
class Server:
    PORT = int(env.get("PORT", 8080))
    BIND_ADDRESS = str(env.get("BIND_ADDRESS", "0.0.0.0"))
    PING_INTERVAL = int(env.get("PING_INTERVAL", "1200"))
    HAS_SSL = str(env.get("HAS_SSL", "True").lower()) in ("1", "true", "t", "yes", "y")
    NO_PORT = str(env.get("NO_PORT", "True").lower()) in ("1", "true", "t", "yes", "y")
    FQDN = str(env.get("FQDN", "filetolinkbyarctix.arctixapis.workers.dev"))
    URL = "http{}://{}{}/".format(
        "s" if HAS_SSL else "", FQDN, "" if NO_PORT else ":" + str(PORT)
    )



