import pandas as pd



class Mutate:
    def __init__(self, csvName = 'dummy.csv', panda = False, read = True):
        self.csvName = csvName
        self.csvPath = f'../Data/{self.csvName}'
        self.panda = self.catch_a_panda(panda, read)


    def catch_a_panda(self, panda, read):
        if read:
            return pd.read_csv(self.csvPath, index_col=None)
        return panda



    def make_csv(self):
        self.panda.to_csv(self.csvPath, index=False)


    def add_column_isin(self):
        self.panda['isin'] = self.panda['url'].apply(lambda x: x.split('-')[-1])
        self.make_csv()


    def drop_columns(self, column_list):
        self.panda.drop(column_list, axis=1, inplace=True)
        self.make_csv()


    def make_a_panda(self, from_list):
        return pd.DataFrame(from_list)

    def join_on_column(self, csv_name, column_name):
        join_this = Mutate(csv_name).panda
        to_this = self.panda
        self.panda = pd.merge(join_this, to_this, on=column_name)
        self.make_csv()

    def remove_rows_with_symbol_false(self):
        self.panda = self.panda[self.panda['symbol'] != 'False']
        self.make_csv()


    def join_pandas(self, pandaList):
        panda = [self.panda] + pandaList
        return pd.concat(panda, ignore_index = True)



class PandaStocks:
    def __init__(self, Page):
        self.page = Page.getJSON()['stocks']
        self.pdStocks = pd.DataFrame(self.page)

