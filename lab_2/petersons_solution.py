import threading

list = [1, 2]

class PetersonSolution():
    # Let writer be 0 and reader be 1. Let writer be first, then turn = 0 and other = 1
    turn = 0
    other = 1

    flag = [False, False]
        
    def CriticalRegionEntry(self,*args):
        global list
        # i gives entered process
        i = args[0]

        #if writer entered other process would be 1 and if reader entered other process would be 0.
        PetersonSolution.other = 1 - i

        # flag of index i would be True
        PetersonSolution.flag[i] = True

        # set turn to i
        PetersonSolution.turn = i

        # if other process is already in the critical section prevent process i to enter
        while PetersonSolution.flag[PetersonSolution.other] == True and PetersonSolution.turn == i:
            if i == 0:
                # writer is in waiting
                print("Writer is waiting...")
            else:
                # reader is waiting
                print("Reader is waiting...")
            
        # Critical region
        if i == 0:
            # writer is in critical section
            print("Writer entered critical section...")
            print(f"Writer append {args[1]}")
            list.append(args[1])
        else:
            # reader is in critical section
            print("Reader entered critical section...")
            try:
                print(f"Reader pops {list.pop()}")
            except IndexError:
                print("List is empty")

        PetersonSolution.flag[i] = False

        print(f"list= {list}")

    def main(self):
        #start writer process, appending 5 to list
        writer = threading.Thread(target = self.CriticalRegionEntry, args = (0,5)) 
        writer.start()
        #start reader process, pop out last element fromlist
        reader = threading.Thread(target = self.CriticalRegionEntry, args = (1,)) 
        reader.start()
        
            
if __name__ == "__main__":
    p = PetersonSolution()
    p.main()