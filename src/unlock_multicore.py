from pathlib import Path
import algo_methods
from multiprocessing import Pool, cpu_count
import os

folder_path = Path("libars_c499/")
src_file = "bench_ckt/c499.bench"

def list_files_in_directory(directory):
    # List to store absolute paths of files
    file_paths = []
    
    # Walk through directory and its subdirectories
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            # Construct absolute path of file
            file_path = os.path.abspath(os.path.join(dirpath, filename))
            file_paths.append(file_path)
    
    return file_paths

# Define a function that handles the task for each file
def process_file(file):
    if file.is_file():
        algo_methods.sat(src_file, str(file), max_iter=1000, print_str = f"{file.name} SAT Attack: ")
        algo_methods.appsat(src_file, str(file), max_iter=1000, print_str = f"{file.name} APPSAT Attack: ")
        algo_methods.hamming_sweep(src_file, str(file), max_iter=1000, print_str = f"{file.name} SWEEP Attack: ")

if __name__ == "__main__":
    # Get all files in the directory
    files = [file.resolve() for file in folder_path.rglob('*') if file.is_file()]

    # Use all available CPU cores
    num_workers = cpu_count()

    # Create a pool of workers
    with Pool(num_workers) as pool:
        pool.map(process_file, files)
