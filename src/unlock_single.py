from pathlib import Path
import algo_methods
import os, random
import signal
import threading, resource
from multiprocessing import Pool,cpu_count,freeze_support
from datetime import datetime

src = "bench_ckt/c1355.bench"
obfs = "panda/c1355_4k_muxl_v2_consc.bench"
result = algo_methods.hamming_sweep(src, obfs, print_str=f"{obfs} SAT Attack: ")
print(result)
