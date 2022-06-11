from src.misc import MultiProcessor
from src.web import WebPage
from src.mutateData import PandaStocks, Mutate



class Onvista:
    def __init__(self):
        self.url = 'https://www.onvista.de/aktien/boxes/finder-json?offset='
        self.results = Results(self.url + str(0))
        self.bigPanda = PandaStocks(self.results.page)


    def generate_stocks_list(self):
        max_range_of_results = self.results.maxResults + 50
        urlList = [self.url + str(_) for _ in range(1, max_range_of_results, 50)]

        pandaList = MultiProcessor(self.build_panda, urlList).resultsList

        self.bigPanda.joinPandas(pandaList)
        self.save_data()


    def save_data(self):
        panda = self.bigPanda.pdStocks
        Mutate('stocksList.csv', panda).make_csv()

    def build_panda(self, url):
        page = Results(url).page
        return PandaStocks(page).pdStocks



class Results:
    def __init__(self, url):
        self.page = WebPage(url, 1)
        self.maxResults = self.page.getJSON()['metaData']['totalHits']



class Yahoo:
    def __init__(self, isinList = False):
        if isinList:
            self.searchUrlList = [(f'https://query2.finance.yahoo.com/v1/finance/search?q={isin}&newsQueryId=news_cie_vespa', isin) for isin in isinList]
        self.resultsList = []


    def getSymbols(self):
        self.resultsList = MultiProcessor(self.builtResults, self.searchUrlList, poolsize = 30).resultsList
        self.save_data()


    def save_data(self):
        panda = Mutate(panda=self.resultsList).make_a_panda()
        Mutate('isinSymbolList.csv', panda).make_csv()


    def builtResults(self, args):
        url, isin = args[0], args[1]
        page = WebPage(url, 60)
        symbol_exists = page.getJSON()['quotes']
        return [isin, (symbol_exists[0]['symbol'] if symbol_exists else False)]



