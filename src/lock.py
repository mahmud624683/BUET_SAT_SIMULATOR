import algo_methods
import os

ckt_name=[]
algo_name=["rll","sarlock","antisat","libar","cac"]
keys=["1100011010101100","001010101111000101011101","10011000111110101010111101010101","111111111001010101000000000011111101010111110101"]


for ckt in ckt_name:
    for algo in algo_name:
        for key in keys:
            bit_no = len(key)
            src_file = f"bench_ckt/bench_ckt/{ckt}.bench"
            lk_file =f"{bit_no}bit/c{ckt}_{algo}_{bit_no}k.bench"
            if os.path.exists(lk_file):
                print(f"{lk_file} file already exist")
            else:
                if algo == "rll": algo_methods.RLL(src_file,lk_file,key)
                elif algo == "sarlock": algo_methods.sarlock(src_file,lk_file,key)
                elif algo == "antisat": 
                    bit_no /= 2 
                    key = key[:bit_no]+key[:bit_no]
                    algo_methods.anti_sat(src_file,lk_file,key)
                elif algo == "libar": 
                    src_file = src_file.replace(ckt,ckt+f"_{bit_no}k")
                    algo_methods.libar(src_file,lk_file,key,libar_bit_no=5,rll_file=True)
                else:
                    cac_file = f"obfuscated/cac{bit_no}.bench"
                    algo_methods.cac(src_file,lk_file,cac_file,bit_no)