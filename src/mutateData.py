import pandas as pd


class PandaStocks:
    def __init__(self, Page):
        self.page = Page.getJSON()['stocks']
        self.pdStocks = pd.DataFrame(self.page)

    def joinPandas(self, pandaList):
        panda = [self.pdStocks] + pandaList
        self.pdStocks = pd.concat(panda, ignore_index = True)


class Mutate:
    def __init__(self, csvName, panda = False ):
        self.csvName = csvName
        self.csvPath = f'./Data/{csvName}'
        self.panda = self.catch_the_panda(panda)


    def catch_the_panda(self, panda):
        if panda:
            return panda
        return pd.read_csv(self.csvPath, index_col=None)


    def make_csv(self):
        self.panda.to_csv(self.csvPath, index=False)


    def add_column_isin(self):
        self.panda['isin'] = self.panda['url'].apply(lambda x: x.xplit('-')[-1])
        self.make_csv()


    def drop_columns(self, column_list):
        self.panda.drop(column_list, axis=1, inplace=True)
        self.make_csv()



