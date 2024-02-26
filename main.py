import requests
import time
import json
import os
from config import Text, Area, Per_page


def get_page(page):
    params = {
        'text': Text,
        'area': Area,
        'page': page,
        'per_page': Per_page
    }

    url = 'https://api.hh.ru/vacancies'
    response = requests.get(url, params=params)
    data = response.json()
    return data


def main():
    print(get_page(0))


if __name__ == "__main__":
    main()
