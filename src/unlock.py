from pathlib import Path
import algo_methods
import os, random
import signal
import threading, resource
from multiprocessing import Pool,cpu_count,freeze_support
from datetime import datetime


class ThreadController:
    def __init__(self,algo_name,src_file,obfs_file,rslt_file,file_no):
        self.thread = threading.Thread(target=self.child_thread,args=())
        self.pid = None
        self.algo = algo_name
        self.src = src_file
        self.obfs = obfs_file
        self.rslt = rslt_file
        self.op_running = True
        self.file_no = file_no


    def child_thread(self):
        self.pid = os.getpid()
        print(f"{self.pid} - {self.file_no}. {self.obfs} attacked by : {self.algo}\n")
        if self.algo == "SAT":
            result = algo_methods.sat(self.src, str(self.obfs), print_str=f"{self.obfs} SAT Attack: ")
        elif self.algo == "APPSAT":
            result = algo_methods.appsat(self.src, str(self.obfs), print_str=f"{self.obfs} APPSAT Attack: ")
        else:
            result = algo_methods.hamming_sweep(self.src, str(self.obfs), max_iter=2000, print_str=f"{self.obfs} SWEEP Attack: ") 
            algo_methods.sat(self.src,self.src)

        algo_methods.sat(self.src, str(self.obfs), max_iter=2)
        open(self.rslt, 'a').write(result)
        self.op_running = False

    def start(self):
        self.thread.start()
    def get_op_running(self):
        return self.op_running
    
    def stop(self):
        if self.pid != None:
            try:
                if self.op_running:
                    open(self.rslt, 'a').write(f"{self.obfs} {self.algo}: TIME LIMIT EXCEEDED\n")
                os.kill(self.pid, signal.SIGTERM)
            except:
                print("error in terminating the process\n")
        self.thread.join()

                  
def simulate_queue(file, time_limit = 120*3600):
    file_no,obfs_file, algo_name = file.split(" ")

    src_des = "bench_ckt"
    obfs_des = "non_libar"
    rslt = "src/final_raw_rslt.txt"
    ckt_name = obfs_file.split("_")[0]
    src_file = os.path.join(src_des, ckt_name + ".bench")
    obfs_file = os.path.join(obfs_des, obfs_file)
    
        
    start_time = datetime.now()
    controller = ThreadController(algo_name,src_file,obfs_file,rslt,file_no)
    controller.start()
    while True:
        current_time = datetime.now()
        op_time = (current_time-start_time).total_seconds()
        if op_time>time_limit:
            controller.stop()
            break
        elif not(controller.get_op_running()):
            break
    

def main():
    with open("src/queue.txt", 'r') as file:
        op_list = file.read().split(",")
    
    for i in range(0,len(op_list)):
        op_list[i] = f"{i} {op_list[i]}"
    
    random.shuffle(op_list)
    print("Total file number - ",len(op_list))
    num_workers = 4#cpu_count()
    
    with Pool(num_workers) as pool:
        pool.map(simulate_queue, op_list)
        pool.close()
        pool.join()
        pool.join()


    #standalone attack
    """ for file in files:
        process_file((files[0],no_files[0])) """
    


if __name__ == "__main__":
    freeze_support()
    main()
