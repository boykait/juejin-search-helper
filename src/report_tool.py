from src.conf import key_word
from src.document import Document


class Template_mixin(object):
    """html报告"""
    HTML_TMPL = """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>%(value)sL统计报告</title>
                <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
                <h1 style="font-family: Microsoft YaHei">%(value)s统计报告</h1>
                <p class='attribute'><strong>统计结果共计 : </strong> %(item_num)s 条干货</p>
                <style type="text/css" media="screen">
                  body  { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px;}
                </style>
            </head>
            <body>
                %(tables)s
            </body>
        </html>"""

    TABLE_TMPL = """
        <table  class="table table-condensed table-bordered table-hover">
                <colgroup>
                    <col align='left' />
                    <col align='left' />
                    <col align='right' />
                    <col align='right' />
                    <col align='right' />
                </colgroup>
                <tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
                    <th>序号</th>
                    <th>标签</th>
                    <th>标题</th>
                    <th>点赞数</th>
                    <th>评论数</th>
                </tr>
                %(table_trs)s
            </table>
                """
    TABLE_TR_TMPL = """
                <tr class='failClass warning'>
                    <td>%(index)s</td>
                    <td>%(label)s</td>
                    <td><a href=%(link)s>%(name)s</a></td>
                    <td>%(likeCount)s</td>
                    <td>%(commentCount)s</td>
                </tr>"""


if __name__ == '__main__':
    tables = ''
    html = Template_mixin()

    f = open('../output/' + key_word + '.txt', 'r')
    data_list = []
    data_map = {"": []}
    filtered_map = {}
    for line in f:
        # 去重
        if line in filtered_map:
            continue
        filtered_map[line] = 1
        data_list.append(line)
    for line in data_list:
        label = line.split('#')[0]
        if label in data_map.keys():
            data_map[label].append(line)
        else:
            data_map[label] = []
            data_map[label].append(line)
    for label_data in data_map.values():

        table_trs = ''
        if len(label_data) <= 0:
            continue
        documents = []
        for line in label_data:
            try:
                label = line.split('#')[0]
                sub_line = line.split('#')[len(line.split('#')) - 1]
                name = sub_line.split('@')[0]
                link = sub_line.split('@')[1]
                like_count = sub_line.split('@')[2]
                comment_count = sub_line.split('@')[3]
                doc = Document(label, name, link, int(like_count), comment_count)
                documents.append(doc)
            except IndexError:
                print(IndexError)
            except ValueError:
                print(ValueError)

        # 按照点赞量进行降序排序
        documents = sorted(documents, key=lambda document: document.like_count, reverse=True)
        # 设置到tr行中
        index = 0
        for doc in documents:
            index = index + 1
            table_trs += html.TABLE_TR_TMPL % dict(index=index, label=doc.label, name=doc.name, link=doc.link,
                                                   likeCount=str(doc.like_count),
                                                   commentCount=doc.comment_count)
        table = html.TABLE_TMPL % dict(table_trs=table_trs)
        tables += table

    output = html.HTML_TMPL % dict(value=key_word, tables=tables, item_num=len(data_list))

    # 生成html报告
    with open("../output/" + key_word + ".html", 'wb') as f:
        f.write(output.encode('utf-8'))
