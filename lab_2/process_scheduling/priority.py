# Process with priority of low number has highest priority i.e 0 has highest priority and so on
import pandas as pd

class Priority():
    def __init__(self, arrival_time:list, burst_time:list, priority:list):
        self.no_process = len(burst_time)
        self.processes = pd.DataFrame({
            'process': [f'P{i+1}' for i in range(self.no_process)],
            'arrival_time': arrival_time,
            'burst_time': burst_time,
            'priority': priority,
            'state': ['ready' for _ in range(self.no_process)],
        }).sort_values(by='arrival_time')
        self.processes.index = [i for i in range(self.no_process)]
        self.scheduler = pd.DataFrame({
            'process': [],
            'cpu_arrival_time': [],
            'cpu_leave_time' : [],
        })
        self.final_calculation = pd.DataFrame({
            'process': list(self.processes["process"]),
            'waiting_time': [- a_t for a_t in self.processes["arrival_time"]],
            'turnaround_time': [None for _ in range(self.no_process)],
        })
        self.avg_turnaround_time = None
        self.avg_waiting_time = None
    
    def do_final_calculation(self, index_p, scld):
        self.final_calculation.at[index_p, "waiting_time"] += scld["cpu_arrival_time"]
        self.final_calculation.at[index_p, "turnaround_time"] = self.final_calculation.at[index_p, "waiting_time"] + self.processes.at[index_p, "burst_time"]
    
    def algorithm(self):
        # make cpu time initially at 0
        cpu_time = 0
        # iterate for the no. of jobs
        while not (all([s == "terminated" for s in list(self.processes["state"])])):
            # At any given cpu time, create a temp dataframe that have arrived and in the waiting state
            temp = pd.DataFrame({
                'index': [],
                'process': [],
                'arrival_time': [],
                'burst_time': [],
                'priority': [],
                'state': [],
            })
            for i, P in self.processes.iterrows():
                if P["state"] == 'terminated':
                    continue
                if P["arrival_time"] <= cpu_time:
                    temp.loc[len(temp)] = [i, P["process"], P["arrival_time"], P["burst_time"], P["priority"],'ready']
            
            try:
                # for every job in temp dataframe, find the index of job with highest priority
                i_pj = temp["priority"].idxmin()
                i_p = int(temp.at[i_pj, "index"])

                # Append in the self.scheduler dataframe the prcess, mark that process as done and decrement the job
                self.scheduler.loc[len(self.scheduler)] = [temp.at[i_pj, "process"], cpu_time, cpu_time + temp.at[i_pj, "burst_time"]]
                self.processes.at[i_p, "state"] = "terminated"
                cpu_time += temp.at[i_pj, "burst_time"]
                self.do_final_calculation(i_p, self.scheduler.loc[len(self.scheduler)-1])
            
            except Exception:
                cpu_time += 1
        
        print("Given Processes\n",self.processes)
        print("CPU Scheduling\n", self.scheduler)
        print("Calculation\n",self.final_calculation.sort_values(by="process"))
        self.avg_turnaround_time = round(self.final_calculation["turnaround_time"].mean(),2)
        self.avg_waiting_time = round(self.final_calculation["waiting_time"].mean(),2)
        print(f"Average waiting time = {self.avg_waiting_time}\nAverage turnaround time = {self.avg_turnaround_time}\n")       


class PreemptivePriority():
    def __init__(self, arrival_time:list, burst_time:list, priority:list):
        self.no_process = len(burst_time)
        self.processes = pd.DataFrame({
            'process': [f'P{i+1}' for i in range(self.no_process)],
            'arrival_time': arrival_time,
            'burst_time': burst_time,
            'priority': priority,
            'state': ['ready' for _ in range(self.no_process)],
            'rem_bt': burst_time,
        }).sort_values(by='arrival_time')
        self.processes.index = [i for i in range(self.no_process)]
        self.scheduler = pd.DataFrame({
            'process': [],
            'cpu_arrival_time': [],
            'cpu_leave_time' : [],
        })
        self.final_calculation = pd.DataFrame({
            'process': list(self.processes["process"]),
            'waiting_time': [- a_t for a_t in self.processes["arrival_time"]],
            'turnaround_time': [None for _ in range(self.no_process)],
        })
        self.avg_turnaround_time = None
        self.avg_waiting_time = None
    
    def preempt_running_job(self):
        i_rj = None
        for i, P in self.processes.iterrows():
            if P["state"] == "running":
                i_rj = i
                break
        if not i_rj == None:
            self.processes.at[i_rj, "state"] = "waiting"
    
    def do_final_calculation(self, index_p, scld):
        if self.processes.at[index_p, "state"] == 'terminated':
            self.final_calculation.at[index_p, "waiting_time"] += scld["cpu_arrival_time"]
            self.final_calculation.at[index_p, "turnaround_time"] = self.final_calculation.at[index_p, "waiting_time"] + self.processes.at[index_p, "burst_time"]

        else:
            self.final_calculation.at[index_p, "waiting_time"] -= (scld["cpu_leave_time"] - scld["cpu_arrival_time"])

    def algorithm(self):
        arrival_time = list(self.processes["arrival_time"])
        cpu_time = 0
        count = 1

        while not (all([s == "terminated" for s in list(self.processes["state"])])):
            # At any given cpu time, create a temp dataframe that have arrived and in the waiting state
            temp = pd.DataFrame({
                'index': [],
                'process': [],
                'arrival_time': [],
                'burst_time': [],
                'priority': [],
                'state': [],
                'rem_bt': [],
            })
            for i, P in self.processes.iterrows():
                if P["state"] == 'terminated':
                    continue
                if P["arrival_time"] <= cpu_time:
                    temp.loc[len(temp)] = [i, P["process"], P["arrival_time"], P["burst_time"], P["priority"],P ["state"], P["rem_bt"]]
            
            try:
                # for every job in temp dataframe, find the index of job with highest priority
                i_pj = temp["priority"].idxmin()
                i_pj_index = int(temp.at[i_pj, "index"])
                
                # if the process is already in running state
                if self.processes.at[i_pj_index, "state"] == "running":
                    temp_ct = cpu_time
                    try:
                        if (arrival_time[count] - cpu_time ) <= temp.at[i_pj, "rem_bt"]:
                            self.scheduler.at[len(self.scheduler)-1, "cpu_leave_time"] = arrival_time[count]
                            cpu_time = arrival_time[count]
                        else:
                            self.scheduler.at[len(self.scheduler)-1, "cpu_leave_time"] = cpu_time + temp.at[i_pj, "rem_bt"]
                            cpu_time += temp.at[i_pj, "rem_bt"]
                        if cpu_time >= arrival_time[count]:
                            count += 1
                    except IndexError:
                        self.scheduler.at[len(self.scheduler)-1, "cpu_leave_time"] = cpu_time + temp.at[i_pj, "rem_bt"]
                        cpu_time += temp.at[i_pj, "rem_bt"]
                    scld = self.scheduler.loc[len(self.scheduler)-1]
                    _bt = scld["cpu_leave_time"] - temp_ct

                # if the process is not in running state
                else:
                    self.preempt_running_job()
                    try:
                        if (arrival_time[count] - cpu_time) <= temp.at[i_pj, "rem_bt"]:
                            self.scheduler.loc[len(self.scheduler)] = [temp.at[i_pj, "process"], cpu_time, arrival_time[count]]
                            cpu_time = arrival_time[count]
                        else:
                            self.scheduler.loc[len(self.scheduler)] = [temp.at[i_pj, "process"], cpu_time, cpu_time + temp.at[i_pj, "rem_bt"]]
                            cpu_time += temp.at[i_pj, "rem_bt"]
                        if cpu_time >= arrival_time[count]:
                            count += 1
                    except IndexError:
                        self.scheduler.loc[len(self.scheduler)] = [temp.at[i_pj, "process"], cpu_time, cpu_time + temp.at[i_pj, "rem_bt"]]
                        cpu_time += temp.at[i_pj, "rem_bt"]
                    scld = self.scheduler.loc[len(self.scheduler)-1]
                    _bt = scld["cpu_leave_time"] - scld["cpu_arrival_time"]
                
                if not _bt == temp.at[i_pj, "rem_bt"]:
                    self.processes.at[i_pj_index, "state"] = "running"
                    self.processes.at[i_pj_index, "rem_bt"] -= _bt
                else:
                    self.processes.at[i_pj_index, "state"] = "terminated"
                    self.processes.at[i_pj_index, "rem_bt"] = 0
                self.do_final_calculation(i_pj_index, scld)
            except Exception:
                cpu_time += 1
        
        print(self.scheduler)
        print(self.final_calculation.sort_values(by=["process"]))
        self.avg_turnaround_time = round(self.final_calculation["turnaround_time"].mean(),2)
        self.avg_waiting_time = round(self.final_calculation["waiting_time"].mean(),2)
        print(f"Average waiting time = {self.avg_waiting_time}\nAverage turnaround time = {self.avg_turnaround_time}\n")       

if __name__ == '__main__':
    at = [0, 20, 40, 60, 80]
    bt = [50, 20, 100, 40, 50]
    prty = [5, 3, 1, 4, 2]
    priority1 = Priority(at, bt, prty)
    priority1.algorithm()
