from pathlib import Path
import algo_methods
from multiprocessing import Pool, cpu_count

folder_path = Path("libars_c499/16k/")
src_file = "bench_ckt/c499.bench"

# Define a function that handles the task for each file
def process_file(file):
    if file.is_file():
        algo_methods.sat(src_file, str(file), max_iter=1000, print_str = f"{file.name} SAT Attack: ")
        algo_methods.appsat(src_file, str(file), max_iter=1000, print_str = f"{file.name} APPSAT Attack: ")
        algo_methods.hamming_sweep(src_file, str(file), max_iter=1000, print_str = f"{file.name} SWEEP Attack: ")

if __name__ == "__main__":
    # Get all files in the directory
    files = [file for file in folder_path.iterdir() if file.is_file()]

    # Use all available CPU cores
    num_workers = cpu_count()

    # Create a pool of workers
    with Pool(num_workers) as pool:
        pool.map(process_file, files)
