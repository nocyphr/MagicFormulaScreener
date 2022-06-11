import pandas as pd
from os.path import exists

class PandaStocks:
    def __init__(self, Page):
        self.page = Page.getJSON()['stocks']
        self.pdStocks = pd.DataFrame(self.page)

    def joinPandas(self, pandaList):
        panda = [self.pdStocks] + pandaList
        self.pdStocks = pd.concat(panda, ignore_index = True)


class Mutate:
    def __init__(self, csvName = 'dummy.csv', panda = False ):
        self.csvName = csvName
        self.csvPath = f'./Data/{csvName}'
        self.panda = self.catch_the_panda(panda)


    def catch_the_panda(self, panda):
        if panda:
            return panda

        i_exist = exists(self.csvPath)
        if i_exist:
            return pd.read_csv(self.csvPath, index_col=None)
        if i_exist == False:
            raise FileNotFoundError(f'{self.csvPath} does not seem to exist')


    def make_csv(self):
        self.panda.to_csv(self.csvPath, index=False)


    def add_column_isin(self):
        self.panda['isin'] = self.panda['url'].apply(lambda x: x.xplit('-')[-1])
        self.make_csv()

    def fetch_isin_list(self):
        if 'isin' in self.panda.columns:
            return

    def drop_columns(self, column_list):
        self.panda.drop(column_list, axis=1, inplace=True)
        self.make_csv()


    def make_a_panda(self, from_list):
        return pd.DataFrame(from_list)
