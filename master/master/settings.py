# ==========================================================================================
# Microservice Master API access settings

# Microservice hostname
HOST = '0.0.0.0'
# Microservice port
PORT = 8000
# Logger debug level
DEBUG = False

# Current url of Master
url = f'http://{HOST}:{PORT}'

# URLs of other microservices to work:
# URL of Keeper microservice
KEEPER_URL = 'http://keeper:8002'
# URL of Reaper microservice
REAPER_URL = 'http://reaper:8001'

# ==========================================================================================



