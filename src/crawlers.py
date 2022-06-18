from misc import MultiProcessor
from parameters import *
from web import WebPage


class Onvista(OnvistaParameters):
    def __init__(self):
        super().__init__()
        self.big_panda = Shapeshift(from_webpage=self.page)

    def generate_stocks_list(self):
        url_list = [self.onvista_url(page) for page in range(1, self.max_results, 50)]

        multiprocessor = MultiProcessor(self.build_panda, url_list)
        panda_list = multiprocessor.results_list

        self.big_panda.join_pandas(panda_list)
        self.big_panda.export_csv(self.stocks_file)
        self.clean_stocks_file()

    def build_panda(self, url):
        results_page = OnvistaSearchResults(url).page
        return Shapeshift(from_webpage=results_page).panda

    def clean_stocks_file(self):
        stocks_csv = Shapeshift(from_file=self.stocks_file)
        stocks_csv.extract_isin_into_new_column()
        columns_to_drop = [
            'last',
            'date',
            'nsin',
            'figures',
        ]
        stocks_csv.drop_columns(columns_to_drop)


class Yahoo(YahooParameters):
    def __init__(self):
        super().__init__()
        self.results_list = []
        self.symbol_dictionary = self.create_symbol_dictionary()
        self.url_arguments = self.create_argument_list()

    def get_symbols(self):
        multiprocessor = MultiProcessor(self.build_results, self.url_arguments, poolsize=38)
        self.results_list = multiprocessor.results_list
        if self.results_list:
            self.save_new_isins_to_file()

        Shapeshift(from_file=self.isin_file).join_isinlist_to_stocks_list()

    def save_new_isins_to_file(self):
        isin_base = Shapeshift(from_file=self.isin_file)
        isin_addon = Shapeshift(from_list=self.results_list)

        columns_dictionary = {
            0: 'isin',
            1: 'symbol'
        }

        isin_addon.rename_panda_columns(columns_dictionary)
        isin_base.join_pandas([isin_addon.panda])
        isin_base.export_csv(self.isin_file)

    def build_results(self, args):
        url, isin = args[0], args[1]

        isin_list = self.isin_keys()
        symbol_dictionary = self.symbol_dictionary

        if isin not in isin_list:
            page = WebPage(url, 120)
            symbol_exists = page.getJSON()['quotes']
            print(f'{isin}: {symbol_exists}')
            return [isin, (symbol_exists[0]['symbol'] if symbol_exists else False)]

        symbol = symbol_dictionary[isin]
        return [isin, symbol]
