from src.document import Document


class Template_mixin(object):
    """html报告"""
    HTML_TMPL = """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>MySQL统计报告</title>
                <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
                <h1 style="font-family: Microsoft YaHei">MySQL统计报告</h1>
                <p class='attribute'><strong>统计结果 : </strong> %(value)s</p>
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
                    <col align='right' />
                    <col align='right' />
                    <col align='right' />
                </colgroup>
                <tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
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
                    <td>%(label)s</td>
                    <td><a href=%(link)s>%(name)s</a></td>
                    <td>%(likeCount)s</td>
                    <td>%(commentCount)s</td>
                </tr>"""


if __name__ == '__main__':
    tables = ''
    html = Template_mixin()

    f = open('../output/mysql.txt', 'r')
    data_list = []
    data_map = {"": []}
    for line in f:
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
                sub_line = line.split('#')[1]
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
        for doc in documents:
            table_trs += html.TABLE_TR_TMPL % dict(label=doc.label, name=doc.name, link=doc.link,
                                                   likeCount=str(doc.like_count),
                                                   commentCount=doc.comment_count)
        table = html.TABLE_TMPL % dict(table_trs=table_trs)
        tables += table

    output = html.HTML_TMPL % dict(value='mysql', tables=tables)

    # 生成html报告
    with open("../output/mysql.html", 'wb') as f:
        f.write(output.encode('utf-8'))
