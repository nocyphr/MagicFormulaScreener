from multiprocessing.dummy import Pool as ThreadPool
from web import WebPage
from mutateData import Mutate



class MultiProcessor:
    def __init__(self, the_function, the_list, poolsize = 50):
        self.pool = ThreadPool(poolsize)
        self.results_list = self.pool.map(the_function, the_list)



class OnvistaParameters:
    def __init__(self):
        self.parameters = {
            'url': 'https://www.onvista.de/aktien/boxes/finder-json?offset=',
            'results': OnvistaSearchResults('https://www.onvista.de/aktien/boxes/finder-json?offset=0'),
            'save_as': 'stocksList.csv'
        }


    def results(self):
        return self.parameters['results']


    def page(self):
        results = self.results()
        return results.page


    def max_results(self):
        results = self.results()
        return results.max_results + 50


    def url(self, page):
        return self.parameters['url'] + str(page)


    def save_as(self):
        return self.parameters['save_as']



class OnvistaSearchResults:
    def __init__(self, url):
        self.page = WebPage(url, 1)
        self.max_results = self.page.getJSON()['metaData']['totalHits']



class YahooParameters:
    def __init__(self):
        self.file_names = {
            'stocksList': 'stocksList.csv',
            'symbolList': 'isinSymbolList.csv',
        }

        self.iterables = {
            'symbol_dictionary': self.create_symbol_dictionary(),
            'url_arguments': self.create_argument_list()
        }

    def create_symbol_dictionary(self):
        symbol_file_name = self.file_names['symbolList']
        try:
            symbol_panda = Mutate(symbol_file_name).panda

            isin_column = list(symbol_panda['isin'])
            symbol_column = list(symbol_panda['symbol'])

            if isin_column:
                symbol_dictionary = {i[0]: i[1] for i in zip(isin_column, symbol_column)}
                return symbol_dictionary

            if not isin_column:
                return {}

        except:
            empty_file = open(symbol_file_name, 'w+')
            empty_file.write('isin,symbol')
            empty_file.close()
            return {}

    def create_argument_list(self):
        isin_list = self.isin_list()

        url_first_part = 'https://query2.finance.yahoo.com/v1/finance/search?q='
        url_last_part = '&newsQueryId=news_cie_vespa'
        url_list = []

        for isin in isin_list:
            url = url_first_part + isin + url_last_part
            arguments = (url, isin)
            url_list += [arguments]

        return url_list


    def isin_list(self):
        isin_file_name = self.file_names['stocksList']
        isin_from_stocks_list = IsinList(isin_file_name).isin_list

        return isin_from_stocks_list

    def name_of_symbol_file(self):
        return self.file_names['symbolList']

    def symbol_dictionary(self):
        return self.iterables['symbol_dictionary']

    def isin_keys(self):
        symbol_dictionary = self.symbol_dictionary()
        return symbol_dictionary.keys()

    def url_arguments(self):
        return self.iterables['url_arguments']

# Ugly hard coded filename
class IsinList:
    def __init__(self, csvName):
        self.isinSymbolList = Mutate('isinSymbolList.csv').panda
        self.stocks_list = Mutate(csvName).panda
        if 'isin' in self.stocks_list.columns:

            isin_series_stocks_list = set(i for i in self.stocks_list['isin'].values)
            isin_series_symbol_list = set(i for i in self.isinSymbolList['isin'].values)

            self.isin_list = list(isin_series_stocks_list - isin_series_symbol_list) + list(isin_series_symbol_list - isin_series_stocks_list)
            print(f'now starting lookup for {len(self.isin_list)} missing entries')
        else:
            raise ValueError(f'{csvName} does not contain a column "isin"')