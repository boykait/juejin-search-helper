class Document(object):
    def __init__(self, label, name, link, like_count, comment_count):
        self.label = label
        self.name = name
        self.link = link
        self.like_count = like_count
        self.comment_count = comment_count

    def get_like_count(self):
        return self.like_count
