import vk_api
import json
import os
from dotenv import load_dotenv

load_dotenv()

_VK_TOKEN = os.getenv('VK_TOKEN', '')

vk_session = vk_api.VkApi(token=_VK_TOKEN)
vk = vk_session.get_api()


def get_all_posts(domain):
    return vk.wall.get(domain=domain, extended=1)


def save_data_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_json_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_all_posts_ids(domain):
    data = get_all_posts(domain)
    return [item['id'] for item in data['items']]


def get_id(filename):
    data = get_json_data(filename)
    return data.get('items')[0].get('from_id')


def get_all_comments(domain, owner_id):
    ids  = get_all_posts_ids(domain)
    data = []
    for post_id in ids:
        data.append(vk.wall.getComments(owner_id=owner_id, post_id=post_id, count=100))
    with open('data/vk_comments.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_comments_as_list():
    with open('data/vk_comments.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    all_comments = []
    for post in data:
        for item in post.get('items', []):
            text = item.get('text', '').strip()
            if text:
                all_comments.append(text)
    return all_comments
