from pathlib import Path
import algo_methods
from multiprocessing import Pool, cpu_count
import os
import resource,signal

folder_path = Path("libars_c1355/")
src_file = "bench_ckt/c1355.bench"
memory_limit_gb = 4  # Memory limit per process (in GB)

def limit_memory():
    soft_limit = memory_limit_gb * 1024 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (soft_limit, soft_limit))


def memory_limited_attack(file):
    limit_memory()

    try:
        algo_methods.hamming_sweep(src_file, str(file), max_iter=1000, print_str=f"{file.name} SWEEP Attack: ", show_key=False)
    except algo_methods.OutOfMemoryException:
        print(f"{file.name} Hamming Sweep: C++ memory limit exceeded, continuing with next file")

    

def process_file(file):
    if file.is_file():
        algo_methods.sat(src_file, str(file), max_iter=1000, print_str = f"{file.name} SAT Attack: ", show_key = False)
        algo_methods.appsat(src_file, str(file), max_iter=1000, print_str = f"{file.name} APPSAT Attack: ", show_key = False)
        #algo_methods.hamming_sweep(src_file, str(file), max_iter=1000, print_str = f"{file.name} SWEEP Attack: ", show_key = False)


if __name__ == "__main__":
    
    files = [file.resolve() for file in folder_path.rglob('*') if file.is_file()]

    # Use all available CPU cores
    num_workers = cpu_count()
    with Pool(num_workers) as pool:
        pool.map(process_file, files)

    # Use all available CPU cores
    """ num_workers = 1
    with Pool(num_workers) as pool:
        pool.map(memory_limited_attack, files) """
