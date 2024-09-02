import algo_methods
import converts

'''
------------- unlocking --------------- 
    --sat = Boolean Satisfiability        
    --appsat = Approximate SAT                        
    --sweep = Sweep Attack S.Bhunia                                                
-------------- locking ----------------   
    --rll = Random Logic Locking                                           
    --sarlock = SARLOCK  
    --libar = LiBAR                                          
'''
def unlock(algo,org_ckt_ls,obs_ckt_ls):
    if algo == "sat":
        algo_methods.sat(org_ckt_ls,obs_ckt_ls)
    elif algo == "appsat":
        algo_methods.appsat(org_ckt_ls,obs_ckt_ls)
    elif algo == "sweep":
        algo_methods.hamming_sweep(org_ckt_ls,obs_ckt_ls,max_iter=1000)
    else:
        print("Wrong Algorithm Name")

if __name__ == "__main__":

    algo = "sat"
    #algo = "appsat"
    #algo = "sweep"

    org_ckt_ls = "bench_ckt/c6288.bench"
    obs_ckt_ls = "src/c6288_antisat_32k.bench"
    #obs_ckt_ls = "obfuscated/c432_libar_unrolled.bench"
    key_str = "101111011001100"
    libar_percent = 0.3
    unlock(algo,org_ckt_ls,obs_ckt_ls)
    print("key= 11000100010100010010111100110000")
    #convert CKT
    #algo_methods.convert_bench2verilog("obfuscated/c432_libar.bench")
    

    

