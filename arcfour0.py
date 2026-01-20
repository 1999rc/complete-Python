import sys 
import time 
from concurrent import futures 
from random import randrange 
from arcfour import arcfour

Jobs=12 
Size=2**18 

Key=b'Twas brilling,and the slithy toves\nDid gyre'
Status='{} workkers,elapsed time: {:.2f}s'

def arcfour_test(size,key):
    in_text=bytearray(randrange(256)for i in range(size))
    cypher_text=arcfour(key,in_text)
    out_text=arcfour(key,cypher_text)
    assert in_text==out_text,'Failed arcfour_test'
def main(workers=None):
    if workers:
        workers=int(workers)
    t0=time.time()
    with futures.ProcessPoolExecutor(workers)as executor:
        actual_wotkers=executor._max_workers 
        to_do=[]
        for i in range(Jobs,0,-1):
            size=Size + int(Size/ Jobs * (i - Jobs/2))
            job=executor.submit(arcfour_test,size,Key)
            to_do.append(job)
        for future in futures.as_completed(to_do):
            res=future.result()
            print('{:.1f} KB'.format(res/2**10))
    print(Status.format(actual_wotkers,time.time()-t0))
if __name__=='__main__':
    if len(sys.argv)==2:
        workers=int(sys.argv[1])
    else:
        workers=None 
    main(workers)
