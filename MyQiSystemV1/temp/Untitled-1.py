import multiprocessing as mp
from multiprocessing import Pool

def f(x):
    for i in range(100000000):
        a1=i

    return x*x

if __name__ == '__main__':
    mp.set_start_method('spawn')
    import time
    t0 = time.time()
    with Pool(4) as p:
        print(p.map(f, [1, 2, 3]))
    elapsed = time.time()-t0
    msg = "{:.2f}s"
    print(msg.format(elapsed))



