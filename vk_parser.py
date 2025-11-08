import vk_api
import json

session = vk_api.VkApi(token="vk1.a.yCytmim7U3QRgYeogjgYrsYptqA2UTLIQsA-Q660Nl_PUks_KF07_OFHgGEFvpa-1EEt2dymBznFmsetyJ_y30vzVvsPrC4UowxIt4J_i-0qNp5meWgoeHcSTTi8A1bDw0Vuzzs9pMlXRBzFY45OKXNtz2p2vytIrF3wpqSdWjRuKy2wL1zELPMAHpJE3Qx35tzAh0Arg28WNkJ6Tr5RiA")
vk = session.get_api()

def get_all_posts(domain):
    data = vk.wall.get(domain=domain, extended=1)
    return data

def save_data_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_json_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_all_posts_ids(domain):
    data = get_all_posts(domain)
    posts_ids = [item['id'] for item in data['items']]
    return posts_ids

def get_id(filename):
    data = get_json_data(filename)
    return data.get("items")[0].get("from_id")

def get_all_comments(domain, owner_id):
    with open('data/comments.json', 'w', encoding='utf-8') as f:
        ids = get_all_posts_ids(domain)
        data = []
        for i in ids:
            data.append(vk.wall.getComments(owner_id=owner_id, post_id = i, count = 100))
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_comments_as_list():
    with open('data/comments.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        all_comments = []
        for i in data:
            for j in i.get('items', []):
                all_comments.append(j.get('text', ''))
    return all_comments

save_data_to_json(get_all_posts("evakorr"), 'data/vk_posts.json')
get_all_comments('evakorr', get_id("data/vk_posts.json"))
get_comments_as_list()

