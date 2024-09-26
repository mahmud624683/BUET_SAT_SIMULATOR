import algo_methods
import os
import resource,signal

folder_path = "libars_c1355"
src_file = "bench_ckt/c1355.bench"


for dirpath, _, filenames in os.walk(folder_path):
    for filename in filenames:
        # Construct absolute path of file
        lk_file = os.path.abspath(os.path.join(dirpath, filename))
        algo_methods.sat(src_file, lk_file, max_iter=1000, print_str = f"{filename} SAT Attack: ", show_key = False)
        algo_methods.appsat(src_file, lk_file, max_iter=1000, print_str = f"{filename} APPSAT Attack: ", show_key = False)
        #algo_methods.hamming_sweep(src_file, lk_file, max_iter=1000, print_str = f"{filename} SWEEP Attack: ", show_key = False)
