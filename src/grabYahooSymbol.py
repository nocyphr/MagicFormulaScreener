from misc import MultiProcessor, YahooParameters
from web import WebPage
from mutateData import Mutate



class Yahoo:
    def __init__(self):
        self.parameters = YahooParameters()
        self.results_list = []


    def get_symbols(self):
        url_arguments = self.parameters.url_arguments()

        multiprocessor = MultiProcessor(self.build_results, url_arguments, poolsize=38)
        self.results_list = multiprocessor.results_list

        self.save_data()


    def save_data(self):
        symbol_file_name = self.parameters.name_of_symbol_file()
        base_panda = Mutate(symbol_file_name)

        mutate_panda = Mutate(panda=self.results_list, read=False)
        append_panda = mutate_panda.make_a_panda()

        joined_panda = base_panda.join_pandas(append_panda)
        joined_panda = Mutate(symbol_file_name, joined_panda, False)

        joined_panda.make_csv()



    def build_results(self, args):
        url, isin = args[0], args[1]

        isin_list = self.parameters.isin_keys()
        symbol_dictionary = self.parameters.symbol_dictionary()

        if isin not in isin_list:
            print(isin)
            page = WebPage(url, 120)
            symbol_exists = page.getJSON()['quotes']
            return [isin, (symbol_exists[0]['symbol'] if symbol_exists else False)]

        symbol = symbol_dictionary[isin]
        print(symbol)
        return [isin, symbol]


Yahoo().get_symbols()