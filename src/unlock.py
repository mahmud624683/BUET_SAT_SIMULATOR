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
        self.file = obfs_file
        self.rslt = rslt_file
        self.op_running = True
        self.file_no = file_no


    def child_thread(self):
        self.pid = os.getpid()
        print(f"{self.pid} - {self.file_no}. {self.file.name} attacked by : {self.algo}\n")
        if self.algo == "SAT Attack":
            result = algo_methods.sat(self.src, str(self.file), print_str=f"{self.file.name} SAT Attack: ")
        elif self.algo == "APPSAT Attack":
            result = algo_methods.appsat(self.src, str(self.file), print_str=f"{self.file.name} APPSAT Attack: ")
        else:
            result = algo_methods.hamming_sweep(self.src, str(self.file), max_iter=2000, print_str=f"{self.file.name} SWEEP Attack: ") 
            algo_methods.sat(self.src,self.src)

        algo_methods.sat(self.src, str(self.file), max_iter=1)
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
                    open(self.rslt, 'a').write(f"{self.file.name} {self.algo}: TIME LIMIT EXCEEDED\n")
                os.kill(self.pid, signal.SIGTERM)
            except:
                print("error in terminating the process\n")
        self.thread.join()

def limit_memory(memory_limit_percent, filename):
    
    soft_limit = memory_limit_percent*(1024**3)
    memory_info = os.popen('free -b').readlines()
    available_memory = int(memory_info[1].split()[3]) # Extract available memory (in bytes)
    if available_memory<soft_limit:
        soft_limit = available_memory
    print("{} process was allocated {}GB".format(filename, soft_limit/(1024**3)))
    resource.setrlimit(resource.RLIMIT_AS, (soft_limit, soft_limit))

def memory_limit_exceeded(signup, frame):
    raise MemoryError("Memory limit exceeded\n")

def process_file(process_file, time_limit = 3*3600):
    file, file_no = process_file
    #signal.signal(signal.SIGXCPU, memory_limit_exceeded)
    #limit_memory(4, file.name)

    src_des = "bench_ckt"
    rslt = "src/raw_rslt6.txt"
    ckt_name = (file.name).split("_")[0]
    src_file = os.path.join(src_des, ckt_name + ".bench")
    
    if file.is_file():
        algo_name = ["SAT Attack", "APPSAT Attack", "SWEEP Attack"]
        random.shuffle(algo_name)

        for algo in algo_name:           
            start_time = datetime.now()
            controller = ThreadController(algo,src_file,file,rslt,file_no)
            controller.start()
            while True:
                current_time = datetime.now()
                op_time = (current_time-start_time).total_seconds()
                if op_time>time_limit:
                    controller.stop()
                    break
                elif not(controller.get_op_running()):
                    break
                  


# Main Function
def main():
    with open("src/queue.txt", 'r') as file:
        op_list = file.read().split(",")
    
    
    folder_path = Path("hlibar")
    #folder_path = Path("obfuscated_ckt/libars")
    files = [file.resolve() for file in folder_path.rglob('*') if file.name in op_list]
    #files = [file.resolve() for file in folder_path.rglob('*') if file.is_file()]
    no_files = range(len(files))
    random.shuffle(files)
    # Use all available CPU cores
    print("Total file number - ",len(files))
    num_workers = 6#cpu_count()
    with Pool(num_workers) as pool:
        pool.map(process_file, zip(files,no_files))
        pool.close()
        pool.join()
        pool.join()


    #standalone attack
    """ for file in files:
        process_file((files[0],no_files[0])) """
    


    


if __name__ == "__main__":
    freeze_support()
    main()
