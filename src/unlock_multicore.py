from pathlib import Path
import algo_methods
import os
import signal,resource
import threading
from multiprocessing import Pool,cpu_count,freeze_support
from datetime import datetime

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
        self.pid = os.getpid()
        print(f"{self.pid} - {self.file.name} attacked by : {self.algo}\n")
        if self.algo == "SAT Attack":
            result = algo_methods.sat(self.src, str(self.file), max_iter=1000, print_str=f"{self.file.name} SAT Attack: ")
        elif self.algo == "APPSAT Attack":
            result = algo_methods.appsat(self.src, str(self.file), max_iter=1000, print_str=f"{self.file.name} APPSAT Attack: ")
        else:
            result = algo_methods.hamming_sweep(self.src, str(self.file), max_iter=1000, print_str=f"{self.file.name} SWEEP Attack: ")
        
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
    mem_total = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    soft_limit = int(memory_limit_percent * mem_total)
    memory_info = os.popen('free -b').readlines()
    available_memory = int(memory_info[1].split()[6]) # Extract available memory (in bytes)
    if available_memory<soft_limit:
        soft_limit = available_memory
    print("{} process was allocated {}GB".format(filename, soft_limit/(1024**2)))
    resource.setrlimit(resource.RLIMIT_AS, (soft_limit, soft_limit))

def memory_limit_exceeded(signum, frame):
    raise MemoryError("Memory limit exceeded\n")


def process_file(file, time_limit = 1800, memory_limit = 0.5):
    signal.signal(signal.SIGXCPU, memory_limit_exceeded)
    limit_memory(memory_limit, file.name)

    src_des = "bench_ckt"
    rslt = "src/raw_rslt.txt"
    ckt_name = (file.name).split("_")[0]
    src_file = os.path.join(src_des, ckt_name + ".bench")

    if file.is_file():
        algo_name = []
        #algo_name += ["SAT Attack", "APPSAT Attack"]#
        algo_name += ["SWEEP Attack"]
        for algo in algo_name:
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
            
            


# Main Function
def main():
    folder_path = Path("libars/")
    files = [file.resolve() for file in folder_path.rglob('*') if file.is_file()]

    # Use all available CPU cores
    num_workers = 2#cpu_count()
    with Pool(num_workers) as pool:
        pool.map(process_file, files)
        pool.close()
        pool.join()
    
    #single core
    """ for file in files:
        process_file(file,1200)
 """


if __name__ == "__main__":
    main()
