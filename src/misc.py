from multiprocessing.dummy import Pool as ThreadPool



class MultiProcessor:
    def __init__(self, theFunction, theList, poolsize = 50):
        self.pool = ThreadPool(poolsize)
        self.resultsList = self.pool.map(theFunction, theList)

