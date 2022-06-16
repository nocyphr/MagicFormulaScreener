from misc import MultiProcessor, OnvistaParameters, OnvistaSearchResults
from mutateData import PandaStocks, Mutate



class Onvista:
    def __init__(self):
        self.parameters = OnvistaParameters()
        page = self.parameters.page()
        self.big_panda = PandaStocks(page).pdStocks


    def generate_stocks_list(self):
        max_range_of_results = self.parameters.max_results()
        url_list = [self.parameters.url(page) for page in range(1, max_range_of_results, 50)]

        multiprocessor = MultiProcessor(self.build_panda, url_list)
        panda_list = multiprocessor.results_list

        mutate_panda = Mutate(panda=self.big_panda, read=False)
        self.big_panda = mutate_panda.join_pandas(panda_list)

        self.save_data()
        self.clean_dataset()


    def save_data(self):
        save_as = self.parameters.save_as()
        panda = self.big_panda
        save = Mutate(csvName=save_as, panda=panda, read=False)
        save.make_csv()


    def build_panda(self, url):
        results_page = OnvistaSearchResults(url).page
        return PandaStocks(results_page).pdStocks


    def clean_dataset(self):
        save_as = self.parameters.save_as()
        mutate_panda = Mutate(save_as)

        mutate_panda.add_column_isin()
        mutate_panda.drop_columns(['last', 'date', 'nsin', 'figures'])



# Onvista().generate_stocks_list() -> run from bashfile