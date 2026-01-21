import importlib 
import sys 
import resource 

Num_vectors=10**7 

if len(sys.argv)==2:
    module_name=sys.argv[1].replace('.py','')
    module=importlib.import_module(module_name)
else:
    print('Usage: {} <vector-module-totest>'.format())
    sys.exit(1)
fmt='Selected Vector2d type: {.__name__}.{__name__}'
print(fmt.format(module,module.Vector2d))
mem_init=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss 
print('Cearing {:,} Vector2d instances'.format(Num_vectors))

vectors=[module.Vector2d(3.0,4.0)for i in range(Num_vectors)]

mem_final=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss 
print('initial RAM usage: {:14,}'.format(mem_init))
print('Final RAM usage: {:14,}'.format(mem_final))
