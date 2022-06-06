import pandas as pd
from helpers import WebPage, MultiProcessor

class Onvista:
    def __init__(self):
        self.url = 'https://www.onvista.de/aktien/boxes/finder-json?offset='
        self.results = Results(self.url + str(0))
        self.bigPanda = PandaStocks(self.results.page)

    def buildPandas(self, url):
        page = Results(url).page
        return PandaStocks(page).pdStocks

    def getStockList(self, csvName = False):
        if csvName:
            self.bigPanda.pdStocks = pd.read_csv(csvName, index_col = None)
        if not csvName:
            urlList = [self.url + str(_) for _ in range(1, self.results.maxResults + 50, 50)]
            pandaList = MultiProcessor(self.buildPandas, urlList).resultsList

            self.bigPanda.joinPandas(pandaList)

    def getCSV(self, csvName = 'stocksList.csv'):
        self.bigPanda.pdStocks.to_csv(csvName, index= False)



class Results:
    def __init__(self, url):
        self.page = WebPage(url, 1)
        self.maxResults = self.page.getJSON()['metaData']['totalHits']



class PandaStocks:
    def __init__(self, Page = False):
        if Page:
            self.page = Page.getJSON()['stocks']
        self.pdStocks = pd.DataFrame(self.page)

    def joinPandas(self, pandaList):
        self.pdStocks = pd.concat([self.pdStocks] + pandaList, ignore_index = True)
        self.cleanData()

    def cleanData(self):
        self.pdStocks['isin'] = self.pdStocks['url'].apply(lambda x: x.split('-')[-1])
        self.pdStocks.drop(['figures', 'last', 'nsin', 'date'], axis = 1, inplace = True)



# o = Onvista()
# o.getStockList()
# o.getCSV()
o = Onvista()
o.getStockList('stocksList.csv')
print(o.bigPanda.pdStocks)
