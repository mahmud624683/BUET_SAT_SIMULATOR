import algo_methods
import os

folder_path = "libars_c499"
src_file = "bench_ckt/c499.bench"


for dirpath, _, filenames in os.walk(folder_path):
    for filename in filenames:
        # Construct absolute path of file
        lk_file = os.path.abspath(os.path.join(dirpath, filename))
        print(f"File: {filename}")
        print("SAT Attack: ", end="")
        algo_methods.sat(src_file, lk_file, max_iter=1000)
        print("APPSAT Attack: ", end="")
        algo_methods.appsat(src_file, lk_file, max_iter=1000)
        print("Sweep Attack: ", end="")
        algo_methods.hamming_sweep(src_file, lk_file, max_iter=1000)
        print('\n')