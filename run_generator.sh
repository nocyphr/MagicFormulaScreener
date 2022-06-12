cd src
python grabOnvista.py
cd ../Data
(head -n 1 stocksList.csv && tail -n +3 stocksList.csv | sort -u) > stocksList2.csv
rm stocksList.csv
mv stocksList2.csv stocksList.csv
rm stocksList2.csv
