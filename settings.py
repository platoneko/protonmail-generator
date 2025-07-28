from datetime import timedelta
import json
import sys
from loguru import logger

# --------------------- May be changed ---------------------
filename = 'proton_accounts.csv'
timezones_filename = 'data folder/timezones.txt'
resolutions_filename = 'data folder/resolutions.json'

# waiting in program logic
two_seconds = 2 # seconds
min_time_to_sleep = 5  # seconds
max_time_to_sleep = 12  # seconds
time_to_sleep_waiting_for_request = 60  # seconds
sleep_between_registrations = 7 # seconds

# Tries count temporary email
tries_count = 10
# Tries count proton mail registration
tries_count_registration = 10
# Use tor proxy
use_tor = True
# If you want to open this file in MS Excel leave ';'
csv_delimiter = ';'

time_format = "%d.%m.%Y %H:%M"

faker_locales = ['it_IT', 'fr_FR', 'de_DE', 'pl_PL', 'es_ES']

# If this parameter is True you can see how all registration works in browser step by step
show_browser_window = True  # True or False
# ------------------ Please don't change -------------------

# Tor settings
tor_path = "utils/tor/tor.exe"
tor_proxy_path = "socks5://127.0.0.1:9150"

# Playwright waiting time
max_playwright_waiting_time = 28_000 # 28 seconds
# Go_to, wait_for_page
min_timeout = 15_000  # ms
max_timeout = 30_000  # ms

# MailApis settings
ZERO = timedelta(0)
SESSION_TIMEOUT_SECONDS = 3600

# protonmail domain
protonmail_domain = '@proton.me'

# Urls
protonmail_registration_address = "https://account.proton.me/signup?plan=free&billing=24&currency=EUR&language=en"
protonmail_login_address = "https://account.proton.me/login?language=en"


# Logging settings
with open("loguru_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

for handler in config["handlers"]:
    if handler["sink"] == "sys.stdout":
        handler["sink"] = sys.stdout

logger.configure(**config)
