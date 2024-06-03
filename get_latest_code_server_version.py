import http.client
import json
from html.parser import HTMLParser
import urllib.parse


host = "github.com"
org = "coder"
repo = "code-server"
path = f"/{org}/{repo}/releases/latest"

conn = http.client.HTTPSConnection(host)
headers = {
    'User-Agent': 'Python-http.client'
}
conn.request("GET", path, headers=headers)
response = conn.getresponse()
if response.status == 302:
    redirect_url = response.getheader('Location')
    parsed_url = urllib.parse.urlparse(redirect_url)
    host = parsed_url.netloc
    path = parsed_url.path

    conn = http.client.HTTPSConnection(host)
    conn.request("GET", path, headers=headers)
    response = conn.getresponse()


html_data = response.read().decode()

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.latest_tag = None
        self.in_span = False

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            for attr in attrs:
                if attr[0] == 'class' and 'ml-1' in attr[1]:
                    self.in_span = True

    def handle_endtag(self, tag):
        if tag == 'span' and self.in_span:
            self.in_span = False

    def handle_data(self, data):
        if self.in_span and self.latest_tag is None:
            self.latest_tag = data.strip()

parser = MyHTMLParser()
parser.feed(html_data)

print(f"{parser.latest_tag}")

