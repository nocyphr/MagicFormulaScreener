from mutateData import PandaStocks, Mutate
from misc import MultiProcessor
from parameters import OnvistaParameters, OnvistaSearchResults, YahooParameters
from web import WebPage



class Onvista(OnvistaParameters):
    def __init__(self):
        super().__init__()

        self.big_panda = PandaStocks(self.page).pdStocks


    def generate_stocks_list(self):
        url_list = [self.onvista_url(page) for page in range(1, self.max_results, 50)]

        multiprocessor = MultiProcessor(self.build_panda, url_list)
        panda_list = multiprocessor.results_list

        mutate_panda = Mutate(panda=self.big_panda, read=False)
        self.big_panda = mutate_panda.join_pandas(panda_list)

        self.save_data()
        self.clean_dataset()


    def save_data(self):
        panda = self.big_panda
        save = Mutate(csvName=self.stocks_file, panda=panda, read=False)
        save.make_csv()


    def build_panda(self, url):
        results_page = OnvistaSearchResults(url).page
        return PandaStocks(results_page).pdStocks


    def clean_dataset(self):
        mutate_panda = Mutate(self.stocks_file)

        mutate_panda.add_column_isin()
        mutate_panda.drop_columns(['last', 'date', 'nsin', 'figures'])


class Yahoo(YahooParameters):
    def __init__(self):
        super().__init__()

        self.results_list = []


    def get_symbols(self):
        url_arguments = self.url_arguments

        multiprocessor = MultiProcessor(self.build_results, url_arguments, poolsize=38)
        self.results_list = multiprocessor.results_list

        self.save_data()


    def save_data(self):
        base_panda = Mutate(csvName=self.isin_file)

        dummy = Mutate(read=False)
        append_panda = dummy.make_a_panda(self.results_list)

        rename_columns_dictionary = {
            0: 'isin',
            1: 'symbol'
        }
        append_panda = Mutate(panda=append_panda, read=False)
        append_panda.rename_panda_columns(rename_columns_dictionary)

        joined_panda = base_panda.join_pandas([append_panda.panda])
        joined_panda = Mutate(self.isin_file, joined_panda, False)

        joined_panda.make_csv()



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