# MagicFormulaScreener
 
## Work in Progress

### implemented: 
- [x] get list of international stocks from onvista  
- [x] make it faster by multiprocessing resultspages  
- [x] join into one big pandas dataframe  
- [x] extract ISIN from url column and put it into it's own column  
- [x] remove unnecessary columns from dataframe  
- [x] generate csv from dataframe  
- [x] generate initial index of ISIN:Symbol via yahoo search API  
- [x] clean up index  
- [x] fill in blanks  
- [x] check for false entries
- [ ] write unittests + refactor
- [ ] get number of shares per stock and last price(onvista)  
- [ ] remove dead/unavailable companies  
- [ ] adjust ISIN:Symbol matching method to lookup first in existing index before going to yahoo
- [ ] get fundamentals (yahoo)
- [ ] use torpy to simulate proxy
