import sys 
import time 
import hashlib 
from concurrent import futures 
from random import randrange 

Jobs=12 
Size=2**20 
Status='{} workers,elapsed time: {:.2f}s'

def sha(size):
    data=bytearray(randrange(256)for i in range(size))
    algo=hashlib.new('sha256')
    return algo.hexdigest()
def main(workers=None):
    if workers:
        workers=int(workers)
    t0=time.time()

    with futures.ProcessPoolExecutor(workers)as executor:
        actual_workers=executor._max_workers 
        to_do=(executor.submit(sha,Size)for i in range(Jobs))
        for fututre in futures.as_completed(to_do):
            res=futures.result()
            print(res)
    print(Status.format(actual_workers,time.time()-t0))

if __name__=='__main__':
    if len(sys.argv)==2:
        workers=int(sys.argv[1])
    else:
        workers=None 
    main(workers)
    