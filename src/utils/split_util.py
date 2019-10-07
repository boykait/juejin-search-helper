import pkuseg


def do_document_split(document):
    seg = pkuseg.pkuseg()  # 以默认配置加载模型
    text = seg.cut(document)  # 进行分词
    print(text)


if __name__ == '__main__':
    do_document_split('说起MySQLJavaPHP\Python的查询优化，相信大家收藏了一堆：不能使用SELECT *、不使用NULL字段、合理创建索引、为字段选择合适的数据类型..... 你是否真的理解这些优化技巧？是否理解其背后的工作原理？')
