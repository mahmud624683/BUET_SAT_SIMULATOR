from pathlib import Path
import algo_methods
import os
import platform
import resource
import sys
import multiprocessing as mp
import time
import queue

# Memory Limiter Functions
def memory_limit(percentage: float):
    if platform.system() != "Linux":
        print('Only works on Linux!')
        return
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    mem_total = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')  # e.g. 4015976448
    resource.setrlimit(resource.RLIMIT_AS, (int(mem_total * percentage), hard))

""" def memory(percentage=0.4):
    def decorator(function):
        def wrapper(*args, **kwargs):
            memory_limit(percentage)
            try:
                return function(*args, **kwargs)
            except MemoryError:
                sys.stderr.write('\n\nERROR: Memory Exception\n')
                sys.exit(1)
        return wrapper
    return decorator
 """

def enforce_memory_limit():
    """Sets memory limits for processes"""
    memory_limit(0.4)

# File processing and multiprocessing functions
folder_path = Path("libars/")
src_des = "bench_ckt"
rslt = "src/raw_rslt.txt"

# Worker Process
#@memory(percentage=0.4)  # Set memory limit to 80%
def process_file(file, q, worker_id):
    enforce_memory_limit()
    ckt_name = (file.name).split("_")[0]
    src_file = os.path.join(src_des, ckt_name + ".bench")
    count = 0  # Message counter for monitoring progress
    try:
        if file.is_file():
            result = algo_methods.sat(src_file, str(file), max_iter=1000, print_str=f"{file.name} SAT Attack: ")
            open(rslt, 'a').write(result)
            q.put(f"Worker {worker_id} - SAT done")
            
            result = algo_methods.appsat(src_file, str(file), max_iter=1000, print_str=f"{file.name} APPSAT Attack: ")
            open(rslt, 'a').write(result)
            q.put(f"Worker {worker_id} - APPSAT done")
            
            result = algo_methods.hamming_sweep(src_file, str(file), max_iter=1000, print_str=f"{file.name} SWEEP Attack: ")
            open(rslt, 'a').write(result)
            q.put(f"Worker {worker_id} - SWEEP done")
            
            q.put(f"Worker {worker_id} - Finished Processing")
            time.sleep(1)  # Simulate work delay
    except Exception as e:
        q.put(f"Worker {worker_id} - Error: {e}")

# Watchdog process
def watchdog(q, num_workers, timeout=10.0):
    """
    Monitor worker activity via the queue. If no messages are received within
    the `timeout` period, assume a worker is hanging and issue a termination signal.
    """
    workers_alive = num_workers
    while workers_alive > 0:
        try:
            msg = q.get(timeout=timeout)
            print(f"[WATCHDOG] Received: {msg}")
            if "Finished" in msg or "Error" in msg:
                workers_alive -= 1  # Worker finished or encountered an error
        except queue.Empty:
            print("[WATCHDOG] No response from worker, possibly hanging")
            q.put("KILL WORKER")

# Main Function
def main():
    files = [file.resolve() for file in folder_path.rglob('*') if file.is_file()]

    # Use all available CPU cores
    num_workers = min(len(files), 2)
    q = mp.Queue()  # Communication queue
    with mp.Pool(processes=num_workers) as pool:
        # Start the watchdog process
        wdog = mp.Process(target=watchdog, args=(q, num_workers, 600))
        wdog.daemon = True
        wdog.start()

        # Map the files to the worker processes
        for i, file in enumerate(files):
            pool.apply_async(process_file, args=(file, q, i))

        pool.close()
        pool.join()  # Wait for all worker processes to complete

        print("[MAIN] All processes completed.")
        wdog.join()  # Wait for the watchdog to complete if necessary


if __name__ == "__main__":
    main()
