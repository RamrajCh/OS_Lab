from fcfs import FCFS
from sjf import SJF
from priority import PreemptivePriority, NonPreemptivePriority
from round_robin import RoundRobin

if __name__ == "__main__":
    _at = input("Give arrival time for process in order:\t").split()
    _bt = input("Give burst time for process in order:\t").split()

    a_t = [int(t) for t in _at]
    b_t = [int(t) for t in _bt]

    flag = input("\nWant FCFS Scheduling?(Y/n)")
    if flag == '' or flag.capitalize() == "Y":
        print("~~~~~~~~~~~~~~~FCFS Scheduling~~~~~~~~~~~~~~~~~~~~~\n")
        fcfs = FCFS(a_t, b_t)
        fcfs.algorithm()
    
    flag = input("\nWant SJF Scheduling?(Y/n)")
    if flag == '' or flag.capitalize() == "Y":
        print("~~~~~~~~~~~~~~~SJF Scheduling~~~~~~~~~~~~~~~~~~~~~\n")
        sjf = SJF(a_t, b_t)
        sjf.algorithm()
    
    flag = input("\nWant Priority Scheduling?(Y/n)")
    if flag == '' or flag.capitalize() == "Y":
        print("~~~~~~~~~~~~~~~Priority Scheduling~~~~~~~~~~~~~~~~~~~~~\n")
        _prty = input("Give priority for process in order:\t").split()
        prty = [int(p) for p in _prty]
        print("~~~~~~~~~~~~~~~Non-Preemptive Priority Scheduling~~~~~~~~~~~~~~~~~~~~~\n")
        npp = NonPreemptivePriority(a_t, b_t, prty)
        npp.algorithm()
        print("~~~~~~~~~~~~~~~Preemptive Priority Scheduling~~~~~~~~~~~~~~~~~~~~~\n")
        pp = PreemptivePriority(a_t, b_t, prty)
        pp.algorithm()
    
    flag = input("\nWant Round Robin Scheduling?(Y/n)")
    if flag == '' or flag.capitalize() == "Y":
        print("~~~~~~~~~~~~~~~Round Robin Scheduling~~~~~~~~~~~~~~~~~~~~~\n")
        tq = int(input("Give time quantaum:\t"))

        rr = RoundRobin(a_t, b_t, tq)
        rr.algorithm()