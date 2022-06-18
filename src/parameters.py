from web import WebPage
from mutateData import Mutate



class URL:
    def __init__(self):
        self.onvista_url = lambda x: f'https://www.onvista.de/aktien/boxes/finder-json?offset={x}'
        self.yahoo_url = lambda x: f'https://query2.finance.yahoo.com/v1/finance/search?q={x}&newsQueryId=news_cie_vespa'



class Files(URL):
    def __init__(self):
        super().__init__()
        self.stocks_file = 'stocksList.csv'
        self.isin_file = 'isinSymbolList.csv'

class OnvistaSearchResults:
    def __init__(self, url):
        self.page = WebPage(url, 1)
        self.max_results = self.page.getJSON()['metaData']['totalHits']

class IsinList(Files):
    def __init__(self):
        super().__init__()
        self.isinSymbolList = Mutate(self.isin_file).panda
        self.stocks_list = Mutate(self.stocks_file).panda
        if 'isin' in self.stocks_list.columns:

            isin_series_stocks_list = set(i for i in self.stocks_list['isin'].values)
            isin_series_symbol_list = set(i for i in self.isinSymbolList['isin'].values)

            self.isin_list = list(isin_series_stocks_list - isin_series_symbol_list)
            print(f'now starting lookup for {len(self.isin_list)} missing entries')
        else:
            raise ValueError(f'{self.stocks_file} does not contain a column "isin"')


class OnvistaParameters(Files):
    def __init__(self):
        super().__init__()
        self.results = OnvistaSearchResults(self.onvista_url(0))
        self.max_results = self.results.max_results + 50
        self.page = self.results.page

class YahooParameters(Files):
    def __init__(self):
        super().__init__()
        self.symbol_dictionary = self.create_symbol_dictionary()
        self.url_arguments = self.create_argument_list()


    def create_symbol_dictionary(self):
        try:
            symbol_panda = Mutate(self.isin_file).panda

            isin_column = list(symbol_panda['isin'])
            symbol_column = list(symbol_panda['symbol'])

            if isin_column:
                symbol_dictionary = {i[0]: i[1] for i in zip(isin_column, symbol_column)}
                return symbol_dictionary

            if not isin_column:
                return {}

        except:
            empty_file = open(self.isin_file, 'w+')
            empty_file.write('isin,symbol')
            empty_file.close()
            return {}

    def create_argument_list(self):
        url_isin_tuple_list = [(self.yahoo_url(isin), isin) for isin in self.isin_list()]
        return url_isin_tuple_list


    def isin_list(self):
        return IsinList().isin_list

    def name_of_symbol_file(self):
        return self.isin_file


    def isin_keys(self):
        symbol_dictionary = self.symbol_dictionary
        return symbol_dictionary.keys()

