import time
import timeit

def benchmark_function(func, *args, **kwargs):
    """
    Benchmark the execution time of a given function.
    
    """
    
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time, result


def compare_functions(func1, func2):
    """ Returns faster function and ratio. """
    

    time1 = timeit.timeit(func1, number=1000)  
    time2 = timeit.timeit(func2, number=1000) 

    # Calculate the execution time ratio
    if time1 < time2:
        faster_function = 1
        ratio = time2 / time1
    else:
        faster_function = 2
        ratio = time1 / time2
    return faster_function, ratio
