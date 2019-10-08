import json

import requests

import src.conf as config


def get_data(after):
    url = 'https://web-api.juejin.im/query'
    query_params = json.dumps({
        "extensions": {"query": {"id": "a53db5867466eddc50d16a38cfeb0890"}},
        "perationName": "",
        "query": "",
        "variables": {"type": "ALL", "query": config.key_word, "after": after, "period": "ALL", "first": 20}
    })
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        "X-Agent": "Juejin/Web",
        "Referer": "https://juejin.im/search?query=mysql&type",
        "Origin": "https://juejin.im"
    }
    response = requests.post(url, data=query_params, headers=headers)
    response.encoding = 'utf-8'
    data = json.loads(response.text)
    query_result = []
    for d in data["data"]["search"]["edges"]:
        try:
            entity = d["node"]["entity"]
            if entity["likeCount"] >= config.min_like_count \
                    and entity["commentsCount"] >= config.min_comment_count:
                url = ''
                if not entity["original"]:
                    url = "https://juejin.im/entry/" + entity["id"]
                else:
                    url = entity["originalUrl"]
                query_result.append(
                    entity["title"] + '@' + url + "@%d" % (entity["likeCount"]) + "@%d" % entity["commentsCount"])
        except KeyError as e:
            print(e)
    return query_result


if __name__ == '__main__':
    output_file = open('../output/mysql.txt', 'w+')
    for i in range(config.max_count):
        if i % 20 == 0:
            query_result = get_data(i)
            for data in query_result:
                try:
                    has = False
                    for label in config.labels:
                        if label in data:
                            has = True
                            data = label + '#' + data
                    if not has:
                        data = '其它#' + data
                    output_file.write(data)
                    output_file.write('\n')
                except UnicodeEncodeError as e:
                    print(e)
            output_file.flush()
    output_file.close()
