import pandas as pd
from utils import get_frame_list
from prettytable import PrettyTable

class Optimal():
    def __init__(self, page_reference:list, page_frame_size:int):
        reference = {"Reference": [], "Next": []}
        for i in range(len(page_reference)):
            ref = page_reference[i]
            try:
                next = page_reference.index(ref, i+1) - i
            except Exception as e:
                next = -1
            reference["Reference"].append(ref)
            reference["Next"].append(next)

        self.page_reference = pd.DataFrame(reference)
        self.frame_size = page_frame_size
        S = [None for _ in range(self.frame_size)]
        Next = [-1 for _ in range(self.frame_size)]
        self.frame = pd.DataFrame({"Frame": S, "Next": Next})
        self.page_fault = 0
        self.table = PrettyTable()
        self.table.add_column("page_reference ->", [f"frame {_ + 1} ->" for _ in range(self.frame_size)] + ['',])
    
    def get_victim(self):
        min = self.frame["Next"].min()
        if min < 0:
            return self.frame["Next"].idxmin()
        else:
            return self.frame["Next"].idxmax()
    
    def update_Next(self):
        for i in range(len(self.frame)):
            self.frame.at[i, "Next"] -= 1
    
    def free_frame(self):
        for i, F in self.frame.iterrows():
            if F["Frame"] == None:
                return i
        return None
    
    def check_reference_avaibility(self, ref):
        for i, F in self.frame.iterrows():
            if F["Frame"] == ref:
                return i
        return None

    def algorithm(self):
        for z, reference in self.page_reference.iterrows():
            ref = reference["Reference"] # 1
            Next = reference["Next"] # 8

            # Check if reference is already in frame, if yes, update next and skip
            i_ref = self.check_reference_avaibility(ref)
            if not i_ref == None:
                self.update_Next()
                self.frame.at[i_ref, "Next"] = Next
                self.table.add_column(ref, get_frame_list(self.frame) + [""])
                continue

            # check if there are any free frame i.e. frame["Frame"] = None, then, take that frame and skip
            i_frame = self.free_frame() # 2
            if not i_frame == None:
                self.update_Next()
                self.frame.at[i_frame, "Frame"] = ref
                self.frame.at[i_frame, "Next"] = Next
                self.page_fault += 1
                self.table.add_column(ref, get_frame_list(self.frame) + ["pf"])
                continue
            
            # If no free frame, select victim
            i_victim = self.get_victim() # 0
            self.update_Next()
            self.frame.at[i_victim, "Frame"] = ref
            self.frame.at[i_victim, "Next"] = Next
            self.page_fault += 1
            self.table.add_column(ref, get_frame_list(self.frame) + ["pf"])
        print(self.table)
        print(f"Total Page Fault: {self.page_fault}\n")

            
if __name__ == '__main__':
    pr = '0 4 1 4 2 4 3 4 2 4 0 7 1 4 8 4 3 4'.split()
    pf1 = 3
    pf2 = 5

    print(f"\n Frames = {pf1}\n")
    optimal1 = Optimal(pr, pf1)
    optimal1.algorithm()

    print(f"\n Frames = {pf2}\n")
    optimal2 = Optimal(pr, pf2)
    optimal2.algorithm()