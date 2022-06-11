from multiprocessing.dummy import Pool as ThreadPool



class MultiProcessor:
    def __init__(self, the_function, the_list, poolsize = 50):
        self.pool = ThreadPool(poolsize)
        self.results_list = self.pool.map(the_function, the_list)

