import requests


BASE = 'https://api.telegram.org/bot'


def get_updates(token):
    url_req = f'{BASE}{token}/getUpdates'
    results = requests.get(url_req)
    return results.json()


def send_msg(token, chat_id, text):
    params={'text': text, 'chat_id':chat_id}
    url_req = f"{BASE}{token}/sendMessage"
    results = requests.get(url_req, params=params)
    print(results.json())


def send_msgs(token, chat_ids, text):
    for chat_id in chat_ids:
        send_msg(token=token, chat_id=chat_id, text=text)


def get_chats(token):
    updates = get_updates(token)
    out = {}
    if updates.get('ok', False):
        for message in updates.get('result', []):
            msg = message.get('message', {})
            chat = msg.get('chat', {})
            if not chat:
                continue
            chat_type = chat.get('type', '')
            if chat_type == 'group':
                out[chat['id']] = chat['title']
            else:
                fname = chat.get('first_name', '')
                lname = chat.get('last_name', '')
                out[chat['id']] = f"{fname} {lname}"
    return out
