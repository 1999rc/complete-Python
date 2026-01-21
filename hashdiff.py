import sys 

Max_bits=len(format(sys.maxsize,'b'))
print('%s-bit Python build'% (Max_bits+1))

def hash_diff(o1,o2):
    h1='{:>0{}b}'.format(hash(o1),Max_bits)
    h2='{:>0{}b}'.format(hash(o2),Max_bits)
    diff=''.join('!'if b1 !=b2 else '' for b1,b2 in zip(h1,h2))
    count='!= {}'.format(diff.count('!'))
    width=max(len(repr(o1)),len(repr(o2)),8)
    sep='-'*(width*2 + Max_bits)
    return '{!:{width}} {}\n{:{width}} {} {}\n{!r{width}} {}\n{}'.format(
        o1,h1,'' * width,diff,count,o2,h2,sep,width=width
    )
if __name__=='__main__':
    print(hash_diff(1,1.0))
    print(hash_diff(1.0,1.0001))
    print(hash_diff(1.0001,1.0002))
    print(hash_diff(1.0002,1.0003))