from src.grabData import Onvista, Yahoo

#generate stocksList.csv
onvista = Onvista()
onvista.generate_stocks_list()

#generate isin-list from stocksList.csv -> fetch Symbols
yahoo = Yahoo()
yahoo.get_symbols()

#clean up data, add symbol column
onvista.clean_dataset()