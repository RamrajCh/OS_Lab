import pandas as pd

class RoundRobin():
    def __init__(self, arrival_time:list, burst_time:list, time_quantum:int):
        self.no_process = len(burst_time)
        self.time_quantum = time_quantum
        self.processes = pd.DataFrame({
            'process': [f'P{i+1}' for i in range(self.no_process)],
            'arrival_time': arrival_time,
            'burst_time': burst_time,
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
        cpu_time = 0
        process_queue = []
        for i, P in self.processes.iterrows():
                if P["state"] == 'terminated':
                    continue
                if P["arrival_time"] <= cpu_time:
                    process_queue.append(i)
        while not (all([s == "terminated" for s in list(self.processes["state"])])):
            try:
                i_job = process_queue[0]

                b_t = self.processes.at[i_job, "rem_bt"]
                if b_t > self.time_quantum:
                    cpu_lt = cpu_time + self.time_quantum
                    self.scheduler.loc[len(self.scheduler)] = [self.processes.at[i_job, "process"], cpu_time, cpu_lt]
                    self.processes.at[i_job, "rem_bt"] -= self.time_quantum
                    cpu_time = cpu_lt
                elif b_t <= self.time_quantum:
                    cpu_lt = cpu_time + self.processes.at[i_job, "rem_bt"]
                    self.scheduler.loc[len(self.scheduler)] = [self.processes.at[i_job, "process"], cpu_time, cpu_lt]
                    cpu_time = cpu_lt
                    self.processes.at[i_job, "rem_bt"] = 0
                    self.processes.at[i_job, "state"] = "terminated"
                    process_queue.remove(i_job)

                for i, P in self.processes.iterrows():
                    if P["state"] == 'terminated':
                        continue
                    if P["arrival_time"] <= cpu_time:
                        if i not in process_queue:
                            process_queue.append(i)
                
                if self.processes.at[i_job, "rem_bt"] > 0:
                    process_queue.remove(i_job)
                    process_queue.append(i_job)

                self.do_final_calculation(i_job, self.scheduler.loc[len(self.scheduler)-1])
            except Exception:
                cpu_time += 1
                for i, P in self.processes.iterrows():
                    if P["state"] == 'terminated':
                        continue
                    if P["arrival_time"] <= cpu_time:
                        process_queue.append(i)
        
        print("Given Processes\n",self.processes)
        print("CPU Scheduling\n", self.scheduler)
        print("Calculation\n",self.final_calculation.sort_values(by="process"))
        self.avg_turnaround_time = round(self.final_calculation["turnaround_time"].mean(),2)
        self.avg_waiting_time = round(self.final_calculation["waiting_time"].mean(),2)
        print(f"Average waiting time = {self.avg_waiting_time}\nAverage turnaround time = {self.avg_turnaround_time}\n")       

if __name__ == '__main__':
    at = [0, 20, 40, 60, 80]
    bt = [50, 20, 100, 40, 50]
    tq = 50
    rr = RoundRobin(at, bt, tq)
    rr.algorithm()