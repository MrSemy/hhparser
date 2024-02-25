import requests
import time
import json
import os


def get_page(page):
    params = {
        'text': 'Python developer',
        'area': 1,
        'page': page,
        'per_page': 10
    }

    url = 'https://api.hh.ru/vacancies'
    response = requests.get(url, params=params)
    data = response.json()
    return data


def main():
    print(get_page(0))


if __name__ == "__main__":
    main()
