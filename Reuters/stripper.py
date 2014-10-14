import re
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip(html):
    s = MLStripper()
    s.feed(html)
    t = s.get_data()
    t = re.sub('[^a-zA-Z ]+', '', t.lower())
    return t
