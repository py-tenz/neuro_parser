import requests
import json
from collections import Counter

llama_url = "http://localhost:11434/api/generate"

def generate_response(prompt):
    response = requests.post(
        url=llama_url,
        json={
            "model": "tinyllama",
            "prompt": prompt,
            'stream' : True
        },
        stream=True
    )

    full_response = ""
    for line in response.iter_lines():
        if not line:
            continue
        data = json.loads(line.decode("utf-8"))
        if "response" in data:
            full_response += data["response"]
        if data.get("done", False):
            break

    return full_response.strip()[0:500]

def get_result_stats(bin_list: list):
    counts = Counter(bin_list)
    pos_percent = counts.get("1", 0)/len(bin_list)*100
    neg_percent = counts.get("-1", 0)/len(bin_list)*100
    neutral_percent = counts.get("0", 0)/len(bin_list)*100
    return [round(pos_percent) if pos_percent else 0, round(neg_percent) if neg_percent else 0 , round(neutral_percent) if neutral_percent else 0]

def get_responce_llama(prompt: str):
    return generate_response(f"Is this statement: '{prompt}' positive?")


