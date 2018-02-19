# +-----------------------------------------------------------------------------------------------+
# |  WARNING: Unless you are adding a new config value you should not edit this file instead you  |
# |           create a ./app/config/[your_env].py file to overload these default values           |
# |                                                                                               |
# |           Specify the location of your config in the NETCAT_CONFIG_FILE envrionment var when  |
# |           you run the program. ex. `export NETCAT_CONFIG_FILE=config/dev.py; python run.py`   |
# +-----------------------------------------------------------------------------------------------+

# Enable flask debug mode, gives you nice print-outs when you get an error
DEBUG = False

# Oauth values need to come from your own discord app
OAUTH2_CLIENT_ID = ""
OAUTH2_CLIENT_SECRET = ""

# Discord won't accept localhost as a callback domain
OAUTH2_REDIRECT_URI = 'http://netcat.local/callback'

# Generate your own random string for this its used for prevent tampering with the session cookie
SECRET_KEY = "" 

# Mongo DB information
MONGO_DBNAME = "users"
MONGO_URI = "" # mongodb://user:pass@netcat.us:27017/users

# The id of the server that the app should update ranks on
GUILD_ID = ""
BOT_TOKEN = ""

# API address is used for both the 'bot' and for oauth
DISCORD_API_URL = 'https://discordapp.com/api'

# Shouldn't need to touch these
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__)+'/../../')
APP_BASE = BASE_DIR + "/app"