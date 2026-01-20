import random 
import collections 
import queue 
import argparse 
import time 

Default_number_of_taxis=3 
Default_end_time=180 
Search_duration=5
Tript_duration=20
Departure_interval=5 
#Taxi simulation entry point
Event=collections.namedtuple('Event','time proc action')

def taxi_process(ident,trips,start_time=0):
    '''Yield to simulator isssuing event at each change'''
    time=yield Event(start_time,ident,'leave garage')
    for i in range(trips):
        time=yield Event(time,ident,'pick up passenger')
        time=yield Event(time,ident,'drop off passenger')
    
    yield Event(time,ident,'going home')
class Simulator:
    def __init__(self,procs_map):
        self.events=queue.PriorityQueue()
        self.procs=dict(procs_map)
    
    def run(self,end_time):
        '''Schedule and display event until time is up🙄'''
        for _, proc in sorted(self.procs.items()):
            first_event=next(proc)
            self.events.put(first_event)
        sim_time=0 
        while sim_time < end_time:
            if self.events.empty():
                print('*** end of events ***')
                break 
            current_event=self.events.get()
            sim_time,proc_id,previous_action=current_event
            print('taxi😁',proc_id,proc_id * ' ,',current_event)
            active_proc=self.procs[proc_id]
            next_time=sim_time + compute_duration(previous_action)
            try:
                next_event=active_proc.send(next_time)
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_event)
        else:
            msg='*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))
def compute_duration(previous_action):
    '''Compute action duration using exponential distribution'''
    if previous_action in ['leave garage','drop of pasenger']:
        interval=Search_duration 
    elif previous_action=='pick up pansenger':
        interval=Tript_duration 
    elif previous_action=='going home😪':
        interval=1 
    else:
        raise ValueError('Unknown previous_action: %s'% previous_action)
    return int(random.expovariate(1/interval))+1
def main(end_time=Default_end_time,num_taxis=Default_number_of_taxis,seed=None):
    '''Initialize random generator,build procs and run simulation'''
    if seed is not None:
        random.seed(seed)
    
    taxis={i:taxi_process(i,(i+1)*2,i*Departure_interval)
           for i in range(num_taxis)}
    sim=Simulator(taxis)
    sim.run(end_time)
if __name__=='__main__':

    parser=argparse.ArgumentParser(
        description='Taxi fleet simulator.'
    )
    parser.add_argument('-e','-end-time',type=int,
                        default=Default_end_time,
                        help='simulation end time;default=%s'
                        % Default_end_time)
    parser.add_argument('-s','--seed',type=int,default=None,
                        help='random generator seed (for testing)')
    args=parser.parse_args()
    main(args.end_time,args.taxis,args.seed)

