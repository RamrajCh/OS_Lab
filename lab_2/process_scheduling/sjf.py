import pandas as pd

class SJF():
    def __init__(self, arrival_time:list, burst_time:list):
        self.no_process = len(burst_time)
        self.processes = pd.DataFrame({
            'process': [f'P{i+1}' for i in range(self.no_process)],
            'arrival_time': arrival_time,
            'burst_time': burst_time,
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
        while not (all([s == "terminated" for s in list(self.processes["state"])])):
            # At any given cpu time, create a temp dataframe that have arrived and in the waiting state
            temp = pd.DataFrame({
                'index': [],
                'process': [],
                'arrival_time': [],
                'burst_time': [],
                'state': [],
            })
            for i, P in self.processes.iterrows():
                if P["state"] == 'terminated':
                    continue
                if P["arrival_time"] <= cpu_time:
                    temp.loc[len(temp)] = [i, P["process"], P["arrival_time"], P["burst_time"], 'ready']
             
            try:
                # for every job in temp dataframe, find the shortest job index
                i_sj = temp["burst_time"].idxmin()
                i_p = int(temp.at[i_sj, "index"])

                # Append in the self.scheduler dataframe the prcess, mark that process as done and decrement the job
                self.scheduler.loc[len(self.scheduler)] = [temp.at[i_sj, "process"], cpu_time, cpu_time + temp.at[i_sj, "burst_time"]]
                self.processes.at[i_p, "state"] = "terminated"
                cpu_time += temp.at[i_sj, "burst_time"]
                self.do_final_calculation(i_p, self.scheduler.loc[len(self.scheduler)-1])
            except Exception:
                # No job in the given cpu time
                cpu_time += 1

        print("Given Processes\n",self.processes)
        print("CPU Scheduling\n", self.scheduler)
        print("Calculation\n",self.final_calculation.sort_values(by="process"))
        self.avg_turnaround_time = round(self.final_calculation["turnaround_time"].mean(),2)
        self.avg_waiting_time = round(self.final_calculation["waiting_time"].mean(),2)
        print(f"Average waiting time = {self.avg_waiting_time}\nAverage turnaround time = {self.avg_turnaround_time}\n")
        
if __name__ == '__main__':
    at = [0, 20, 40, 60, 80]
    bt = [50, 20, 100, 40, 50]
    sjf = SJF(at, bt)
    sjf.algorithm()