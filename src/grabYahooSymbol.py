from misc import MultiProcessor, YahooParameters
from web import WebPage
from mutateData import Mutate




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


# Yahoo().get_symbols()