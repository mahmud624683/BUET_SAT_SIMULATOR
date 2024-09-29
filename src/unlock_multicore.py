from pathlib import Path
import algo_methods
import os
import signal
import threading
from multiprocessing import Pool,cpu_count,freeze_support
import time

class ThreadController:
    def __init__(self,algo_name,src_file,obfs_file,rslt_file):
        print("constructor")
        self.thread = threading.Thread(target=self.child_thread,args=())
        self.pid = None
        self.algo = algo_name
        self.src = src_file
        self.file = obfs_file
        self.rslt = rslt_file
        self.op_running = True


    def child_thread(self):
        self.pid = os.getpid()
        print(f"PID - {self.pid} {self.file.name} attacked by {self.algo}")
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

    def stop(self):
        if self.pid != None:
            try:
                if self.op_running:
                    open(self.rslt, 'a').write(f"{self.file.name} {self.algo}: TIME LIMIT EXCEEDED")
                os.kill(self.pid, signal.SIGTERM)
            except:
                print("error in terminating the process")
        self.thread.join()


def process_file(file, time_limit = 300, memory_limit = 0.4):
    src_des = "bench_ckt"
    rslt = "src/raw_rslt.txt"
    ckt_name = (file.name).split("_")[0]
    src_file = os.path.join(src_des, ckt_name + ".bench")

    if file.is_file():
        algo_name = ["SAT Attack", "APPSAT Attack", "SWEEP Attack"]
        for algo in algo_name:
            controller = ThreadController(algo,src_file,file,rslt)
            controller.start()
            time.sleep(time_limit)
            controller.stop()
            


# Main Function
def main():
    folder_path = Path("libars/")
    files = [file.resolve() for file in folder_path.rglob('*') if file.is_file()]

    # Use all available CPU cores
    num_workers = 2#cpu_count()
    with Pool(num_workers) as pool:
        pool.map(process_file, files)



if __name__ == "__main__":
    main()
