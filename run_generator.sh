cd src
echo 'now grabbing stocksList'
python -c 'from crawlers import Onvista; Onvista().generate_stocks_list()'
echo 'switching to Data-Directory'
cd ../Data
echo 'removing duplicate entries in stocksList.csv'
(head -n 1 stocksList.csv && tail -n +3 stocksList.csv | sort -u) > stocksList2.csv
echo 'cleanup'
rm stocksList.csv
mv stocksList2.csv stocksList.csv
echo 'switching to src-Directory'
cd ../src
echo 'now translating ISIN to Symbol'
python -c 'from crawlers import Yahoo; Yahoo().get_symbols()'
echo 'switching to Data-Directory'
cd ../Data
echo 'removing duplicate entries in isinSymbolList.csv'
(head -n 1 isinSymbolList.csv && tail -n +3 isinSymbolList.csv | sort -u) > isinSymbolList2.csv
echo 'cleanup'
rm isinSymbolList.csv
mv isinSymbolList2.csv isinSymbolList.csv
echo 'switching to src-Directory'
cd ../src
echo 'joining isinSymbolList to stocksList on column isin'
python -c 'from mutateData import Mutate; Mutate(csvName="stocksList.csv").join_on_column("isinSymbolList.csv", "isin")'
echo 'switching to Data-Directory'
cd ../Data
echo 'removing entries without ticker symbol from stockslist'
sed -i '/False/d' ./stocksList.csv
echo 'removing duplicate entries in stocksList.csv'
(head -n 1 stocksList.csv && tail -n +3 stocksList.csv | sort -u) > stocksList2.csv
echo 'cleanup'
rm stocksList.csv
mv stocksList2.csv stocksList.csv
echo 'Done'
