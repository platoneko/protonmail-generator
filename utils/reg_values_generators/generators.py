from faker import Faker
from fake_useragent import UserAgent
import random
import string
import re

import settings
from utils.common.file_operations import get_choice_from_text_file, get_choice_from_json

fake = Faker(locale=settings.faker_locales)
ua = UserAgent()


def only_english_letters(text):
    return re.sub(r'[^A-Za-z ]', '', text)


def generate_name_and_lastname() -> str:
    return only_english_letters(fake.first_name())


def generate_password(min_len=17, max_len=24, vals=string.ascii_letters + string.digits) -> str:
    random_number = random.randint(min_len, max_len)
    password = ''.join(random.choices(vals, k=random_number))
    return password


def return_user_data() -> tuple[str, str]:
    password = generate_password()
    username = generate_name_and_lastname()
    username = username + str(random.randint(1000, 999999))
    return username, password


def generate_user_agent():
    # return fake.user_agent()
    return random.choice([ua.opera, ua.edge, ua.chrome, ua.firefox])


def get_timezone():
    return get_choice_from_text_file(settings.timezones_filename)
    # return fake.timezone()

def get_viewport():
    return get_choice_from_json(settings.resolutions_filename)
