from pathlib import Path
import algo_methods
import os, random, time
import signal,resource
import threading
from multiprocessing import Pool,cpu_count,freeze_support
from datetime import datetime

global op_list
op_list = []

class ThreadController:
    def __init__(self,algo_name,src_file,obfs_file,rslt_file):
        self.thread = threading.Thread(target=self.child_thread,args=())
        self.pid = None
        self.algo = algo_name
        self.src = src_file
        self.file = obfs_file
        self.rslt = rslt_file
        self.op_running = True


    def child_thread(self):
        global op_list
        self.pid = os.getpid()
        print(f"{self.pid} - {self.file.name} attacked by : {self.algo}\n")
        if self.algo == "SAT Attack":
            result = algo_methods.sat(self.src, str(self.file), max_iter=1000, print_str=f"{self.file.name} SAT Attack: ")
        elif self.algo == "APPSAT Attack":
            result = algo_methods.appsat(self.src, str(self.file), max_iter=1000, print_str=f"{self.file.name} APPSAT Attack: ")
        else:
            algo_methods.sat(self.src,self.src)
            result = algo_methods.hamming_sweep(self.src, str(self.file), max_iter=1000, print_str=f"{self.file.name} SWEEP Attack: ")
            
        algo_methods.sat("bench_ckt/c17.bench","bench_ckt/c17.bench")
        open(self.rslt, 'a').write(result)
        result_split = result.split(" Attack:")
        op_list.append(result_split[0].strip())
        
        self.op_running = False

    def start(self):
        self.thread.start()
    def get_op_running(self):
        return self.op_running
    
    def stop(self):
        if self.pid != None:
            try:
                if self.op_running:
                    open(self.rslt, 'a').write(f"{self.file.name} {self.algo}: TIME LIMIT EXCEEDED\n")
                os.kill(self.pid, signal.SIGTERM)
            except:
                print("error in terminating the process\n")
        self.thread.join()



def process_file(file, time_limit = 600):
    global op_list
    src_des = "bench_ckt"
    rslt = "src/raw_rslt3.txt"
    ckt_name = (file.name).split("_")[0]
    src_file = os.path.join(src_des, ckt_name + ".bench")

    if file.is_file():
        algo_name = ["SAT Attack", "APPSAT Attack", "SWEEP Attack"]
        random.shuffle(algo_name)

        for algo in algo_name:
            op_name = os.path.basename(file.name)+" "+algo
            if op_name not in op_list:
                start_time = datetime.now()
                controller = ThreadController(algo,src_file,file,rslt)
                controller.start()
                while True:
                    current_time = datetime.now()
                    op_time = (current_time-start_time).total_seconds()
                    if op_time>time_limit:
                        controller.stop()
                        break
                    elif not(controller.get_op_running()):
                        break
            else: print(op_name + " already done")
            


def sweep_attack(file, time_limit = 24*3600):
    global op_list
    src_des = "bench_ckt"
    rslt = "src/raw_rslt3.txt"
    ckt_name = (file.name).split("_")[0]
    src_file = os.path.join(src_des, ckt_name + ".bench")

    if file.is_file():
        op_name = os.path.basename(file.name)+" SWEEP Attack"
        if op_name not in op_list:
            start_time = datetime.now()
            controller = ThreadController("SWEEP Attack",src_file,file,rslt)
            controller.start()
            while True:
                current_time = datetime.now()
                op_time = (current_time-start_time).total_seconds()
                if op_time>time_limit:
                    controller.stop()
                    break
                elif not(controller.get_op_running()):
                    break  
        else:   print(op_name + " already done")        


# Main Function
def main():
    global op_list
    with open('src/op_list.txt', 'r') as file:
        op_list = file.read().split(",")

    folder_path = Path("obfuscated_ckt/libars")
    files = [file.resolve() for file in folder_path.rglob('*') if file.is_file()]
    random.shuffle(files)
    # Use all available CPU cores
    num_workers = 10#cpu_count()
    with Pool(num_workers) as pool:
        pool.map(process_file, files)
        pool.close()
        pool.join()
        pool.join()

    #sweep attack""" 

    for file in files:
        process_file(file)
    


    with open('src/op_list.txt', 'w') as file:
        file.write(",".join(op_list))


if __name__ == "__main__":
    main()
