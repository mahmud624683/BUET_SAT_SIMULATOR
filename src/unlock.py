from pathlib import Path
import algo_methods

folder_path = Path("libars_432/16k/")
src_file = "bench_ckt/c432.bench"

for file in folder_path.iterdir():
    if file.is_file():
        print(f"File: {file.name}")
        print("SAT Attack: ", end="")
        algo_methods.sat(src_file, "libars_432/16k/"+file.name, max_iter=1000)
        print("APPSAT Attack: ", end="")
        algo_methods.appsat(src_file, "libars_432/16k/"+file.name, max_iter=1000)
        print("Sweep Attack: ", end="")
        algo_methods.hamming_sweep(src_file, "libars_432/16k/"+file.name, max_iter=1000)
        print('\n')