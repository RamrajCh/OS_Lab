import pandas as pd
from utils import check_reference_avaibility, free_frame, get_frame_list
from prettytable import PrettyTable

class LRU():
    def __init__(self, page_reference:list, page_frame_size:int):
        self.page_reference = pd.Series(page_reference)
        self.frame_size = page_frame_size
        S = [None for _ in range(self.frame_size)]
        Status = [-1 for _ in range(self.frame_size)]  
        self.frame = pd.DataFrame({"Frame": S, "Status": Status})
        self.page_fault = 0
        self.table = PrettyTable()
        self.table.add_column("page_reference ->", [f"frame {_ + 1} ->" for _ in range(self.frame_size)] + ['',])
    
    def get_victim(self):
        for i, F in self.frame.iterrows():
            if F["Status"] == self.frame_size - 1:
                return i
    
    def update_status(self, s_ref=None):
        if (s_ref == None) or (s_ref == self.frame_size - 1):
            for i in range(len(self.frame)):
                status = self.frame.at[i, "Status"]
                if not status == -1:
                    self.frame.at[i, "Status"] = (status + 1) % self.frame_size
        elif s_ref == 0:
            pass
        else:
            for i in range(len(self.frame)):
                status = self.frame.at[i, "Status"]
                if not status == -1:
                    if status > s_ref:
                        pass
                    elif status < s_ref:
                        self.frame.at[i, "Status"] = status + 1
                    elif status == s_ref:
                        self.frame.at[i, "Status"] = 0


    def algorithm(self):
        for ref in self.page_reference:
            # Check if reference is already in frame, if yes, update status and then skip
            s_ref = check_reference_avaibility(self.frame, ref)
            if not s_ref == None:
                self.update_status(s_ref)
                self.table.add_column(ref, get_frame_list(self.frame) + [""])
                continue

            # check if there are any free frame i.e. frame["Frame"] = None and skip
            i_frame = free_frame(self.frame)
            if not i_frame == None:
                self.update_status()
                self.frame.at[i_frame, "Frame"] = ref
                self.frame.at[i_frame, "Status"] = 0
                self.page_fault += 1
                self.table.add_column(ref, get_frame_list(self.frame) + ["pf"])
                continue
            
            # If no free frame, select victim
            i_victim = self.get_victim()
            self.update_status()
            self.frame.at[i_victim, "Frame"] = ref
            self.page_fault += 1
            self.table.add_column(ref, get_frame_list(self.frame)+ ["pf"])
        print(self.table)
        print(f"Total Page Fault: {self.page_fault}\n")

            


                




if __name__ == '__main__':
    pr = '0 4 1 4 2 4 3 4 2 4 0 7 1 4 8 4 3 4'.split()
    pf1 = 3
    pf2 = 5

    print(f"\n Frames = {pf1}\n")
    lru1 = LRU(pr, pf1)
    lru1.algorithm()

    print(f"\n Frames = {pf2}\n")
    lru2 = LRU(pr, pf2)
    lru2.algorithm()