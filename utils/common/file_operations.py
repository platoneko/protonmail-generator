import csv
import json
import random
import settings


text_lines = []
json_data = []

def create_new_file(first_row):
    with open(settings.filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=settings.csv_delimiter)
        writer.writerow(first_row)


def add_to_file(data):
    with open(settings.filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=settings.csv_delimiter)
        writer.writerow(data)



def get_choice_from_text_file(filename):
    global text_lines
    if len(text_lines) == 0:
        with open(filename, encoding="utf-8") as file:
            text_lines = [line.strip() for line in file if line.strip()]
    return random.choice(text_lines)


def get_choice_from_json(filename):
    global json_data
    if len(json_data) == 0:
        with open(filename, encoding="utf-8") as file:
            json_data = json.load(file)
    return random.choice(json_data)
