import requests
import time
import json
import os
import dotenv
from tele import send_msg
from config import Text, Area, Per_page, Id_of_shed


dotenv.load_dotenv()


def get_page(page):
    params = {
        'text': Text,
        'area': Area,
        'page': page,
        'per_page': Per_page,
        'schedule': Id_of_shed
    }

    url = 'https://api.hh.ru/vacancies'
    response = requests.get(url, params=params)
    data = response.content.decode('utf-8')
    return data


def get_data():
    data_summary = ''
    for page in range(0, 1):
        data = get_page(page)
        time.sleep(0.5)
        if data is None:
            continue
        data_summary += data
    with open('last_results.txt', 'w', encoding='utf-8') as f:
        f.write(data_summary)


def parse_the_answer():
    result_summary = []
    result = {}
    salary_list = {}
    with open('last_results.txt', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data['items']:
        if item['archived']:
            continue
        result['Название'] = item['name']
        result['Ссылка'] = item['alternate_url']
        salary_list = item['salary']
        if salary_list is None:
            continue
        else:
            if salary_list['from'] is None:
                salary_list['from'] = "не указано"
            if salary_list['to'] is None:
                salary_list['to'] = "не указано"
            if salary_list['currency'] is None:
                salary_list['currency'] = ""
            result["ЗП"] = f'{salary_list["from"]} - {salary_list["to"]} ({salary_list["currency"]})'
        result_summary.append(result.copy())
    return result_summary


def vacancies_old_save(text):
    with open('last_vacancies.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(text, ensure_ascii=False).encode('utf-8').decode())


def vacancies_old_load():
    with open('last_vacancies.txt', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            return None
        return data


def main():
    get_data()
    parsed_vacancies = parse_the_answer()
    old_vacancies = vacancies_old_load()
    if old_vacancies is None:
        print('Нет старых данных')
    else:
        for item in parsed_vacancies:
            if item not in old_vacancies:
                text_to_send = f'Название: {item["Название"]}\nЗП: {item["ЗП"]}\nСсылка: {item["Ссылка"]}\n'
                print(text_to_send)
                send_msg(os.environ.get('TOKEN'), os.environ.get('CHAT_ID'), text_to_send)
            else:
                continue
    vacancies_old_save(parsed_vacancies)


if __name__ == "__main__":
    main()
