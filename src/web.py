import requests
from time import sleep



class WebPage:
    def __init__(self, url, retry = 0):
        self.header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
        self.url = url
        self.retry = retry
        self.html = self.getHTML()

    def getHTML(self):
        try:
            response = requests.get(self.url, headers = self.header)

            if response.ok:
                return response
            if self.retry:
                print('i sleep now')
                sleep(self.retry)
                return (self.getHTML())
        except:
            print('sleep for exception')
            sleep(5)
            return self.getHTML()

    def getJSON(self):
        return self.html.json()