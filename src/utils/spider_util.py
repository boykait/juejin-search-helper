import json

import requests


def get_data():
    url = 'https://web-api.juejin.im/query'
    query_params = json.dumps({
        "extensions": {"query": {"id": "a53db5867466eddc50d16a38cfeb0890"}},
        "perationName": "",
        "query": "",
        "variables": {"type": "ALL", "query": "mysql", "after": "", "period": "ALL", "first": "100"}
    })
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        "X-Agent": "Juejin/Web",
        "Referer": "https://juejin.im/search?query=mysql&type",
        "Origin": "https://juejin.im"
    }
    # response = requests.get('https://juejin.im/post/59d83f1651882545eb54fc7e', headers=headers)
    response = requests.post(url, data=query_params, headers=headers)
    response.encoding = 'utf-8'
    # print(response.text)
    data = json.loads(response.text)
    for d in data["data"]["search"]["edges"]:
        try:
            print(d["node"]["entity"]["title"] + ' ' + d["node"]["entity"]["originalUrl"])
        except KeyError as e:
            a = 1


if __name__ == '__main__':
    get_data()
