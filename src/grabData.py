from os.path import exists
from src.misc import MultiProcessor
from src.web import WebPage
from src.mutateData import PandaStocks, Mutate


class Onvista:
    def __init__(self):
        self.url = 'https://www.onvista.de/aktien/boxes/finder-json?offset='
        self.results = Results(self.url + str(0))
        self.save_as = 'stocksList.csv'
        self.big_panda = PandaStocks(self.results.page)

    def generate_stocks_list(self):
        max_range_of_results = self.results.max_results + 50
        url_list = [self.url + str(_) for _ in range(1, max_range_of_results, 50)]

        panda_list = MultiProcessor(self.build_panda, url_list).results_list

        self.big_panda.joinPandas(panda_list)
        self.save_data()

    def save_data(self):
        panda = self.big_panda.pdStocks
        save = Mutate(csvName=self.save_as, panda=panda, read=False)
        save.make_csv()

    def build_panda(self, url):
        page = Results(url).page
        return PandaStocks(page).pdStocks

    def clean_dataset(self):
        Mutate(self.save_as).add_column_isin()
        Mutate(self.save_as).drop_columns(['last', 'date', 'nsin', 'figures'])
        Mutate(self.save_as).join_on_column('isinSymbolList.csv', 'isin')


class Yahoo:
    def __init__(self):
        isin_list = IsinList('stocksList.csv').isin_list
        self.search_url_list = [
            (f'https://query2.finance.yahoo.com/v1/finance/search?q={isin}&newsQueryId=news_cie_vespa', isin) for isin
            in isin_list]
        self.results_list = []

    def get_symbols(self):
        self.results_list = MultiProcessor(self.built_results, self.search_url_list, poolsize=30).results_list
        self.save_data()

    def save_data(self):
        panda = Mutate(panda=self.results_list).make_a_panda()
        Mutate('isinSymbolList.csv', panda).make_csv()

    def built_results(self, args):
        url, isin = args[0], args[1]
        page = WebPage(url, 60)
        symbol_exists = page.getJSON()['quotes']
        return [isin, (symbol_exists[0]['symbol'] if symbol_exists else False)]


class Results:
    def __init__(self, url):
        self.page = WebPage(url, 1)
        self.max_results = self.page.getJSON()['metaData']['totalHits']


class IsinList:
    def __init__(self, csvName):
        self.stocks_list = Mutate(csvName).panda
        if 'isin' in self.stocks_list.columns:
            self.isin_list = [i for i in self.stocks_list['isin']]
        else:
            raise ValueError(f'{csvName} does not contain a column "isin"')



