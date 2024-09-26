import algo_methods
import os
import resource,signal

folder_path = "libars_c1355"
src_file = "bench_ckt/c1355.bench"

memory_limit_mb = 7.5  # Memory limit per process (in GB)

def limit_memory():
    soft_limit = memory_limit_mb * 1024 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (soft_limit, soft_limit))

def memory_limit_exceeded(signum, frame):
    raise MemoryError("Memory limit exceeded")

for dirpath, _, filenames in os.walk(folder_path):
    for filename in filenames:
        #signal.signal(signal.SIGXCPU, memory_limit_exceeded)
        #limit_memory()
        # Construct absolute path of file
        lk_file = os.path.abspath(os.path.join(dirpath, filename))
        print(f"File: {filename}")
        print("SAT Attack: ", end="")
        algo_methods.sat(src_file, lk_file, max_iter=1000)
        print("APPSAT Attack: ", end="")
        algo_methods.appsat(src_file, lk_file, max_iter=1000)
        #print("Sweep Attack: ", end="")
        #algo_methods.hamming_sweep(src_file, lk_file, max_iter=1000)
        print('\n')