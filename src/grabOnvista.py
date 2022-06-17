from misc import MultiProcessor, OnvistaParameters, OnvistaSearchResults
from mutateData import PandaStocks, Mutate



class Onvista(OnvistaParameters):
    def __init__(self):
        super().__init__()

        page = self.page()
        self.big_panda = PandaStocks(page).pdStocks


    def generate_stocks_list(self):
        url_list = [self.url(page) for page in range(1, self.max_results, 50)]

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



Onvista().generate_stocks_list() #-> run from bashfile