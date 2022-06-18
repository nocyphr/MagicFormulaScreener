import pandas as pd

class URL:
    def __init__(self):
        self.onvista_url = lambda x: f'https://www.onvista.de/aktien/boxes/finder-json?offset={x}'
        self.yahoo_url = lambda x: f'https://query2.finance.yahoo.com/v1/finance/search?q={x}&newsQueryId=news_cie_vespa'



class Statics(URL):
    def __init__(self):
        super().__init__()
        self.stocks_file = 'stocksList.csv'
        self.isin_file = 'isinSymbolList.csv'
        self.file_path = lambda x: f'../Data/{x}'



class Shapeshift(Statics):
    def __init__(self, from_file = False, from_panda = False, from_list = False, from_webpage = False):
        super().__init__()
        if from_file:
            self.panda = pd.read_csv(self.file_path(from_file), index_col=None)
        if from_panda:
            self.panda = from_panda
        if from_list:
            self.panda = pd.DataFrame(from_list)
        if from_webpage:
            web_page = from_webpage.getJSON()['stocks']
            self.panda = pd.DataFrame(web_page)

    def export_csv(self, file_name):
        self.panda.to_csv(self.file_path(file_name), index=None)

    def extract_isin_into_new_column(self):
        self.panda['isin'] = self.panda['url'].apply(lambda x: x.split('-')[-1])
        self.export_csv(self.stocks_file)

    def drop_columns(self, list_of_columns):
        self.panda.drop(list_of_columns, axis=1, inplace=True)
        self.export_csv(self.stocks_file)

    def join_isinlist_to_stocks_list(self):
        stocks_panda = Shapeshift(from_file=self.stocks_file).panda
        self.panda = pd.merge(self.panda, stocks_panda, on='isin')
        self.export_csv(self.stocks_file)

    def join_pandas(self, second_panda):
        self.panda = pd.concat([self.panda] +  second_panda, ignore_index = True)

    def rename_panda_columns(self, rename_dictionary):
        self.panda.rename(columns=rename_dictionary, inplace=True)