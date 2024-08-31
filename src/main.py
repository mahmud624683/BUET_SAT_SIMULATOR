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
def lock_unlock(algo,org_ckt_ls,obs_ckt_ls,key_str="",libar_percent=0):
    if algo == "sat":
        algo_methods.sat(org_ckt_ls,obs_ckt_ls)
    elif algo == "appsat":
        algo_methods.appsat(org_ckt_ls,obs_ckt_ls)
    elif algo == "sweep":
        algo_methods.hamming_sweep(org_ckt_ls,obs_ckt_ls,max_iter=1000)
    elif algo == "sarlock":
        algo_methods.sarlock(org_ckt_ls,obs_ckt_ls,key_str)
    elif algo == "rll":
        algo_methods.rll(org_ckt_ls,obs_ckt_ls,key_str)
    elif algo == "libar":
        algo_methods.libar(org_ckt_ls,obs_ckt_ls,key_str,libar_percent)
    elif algo == "antisat":
        algo_methods.anti_sat(org_ckt_ls,obs_ckt_ls,key_str)
    elif algo == "asob":
        algo_methods.asob(org_ckt_ls,obs_ckt_ls,key_str,6)
    else:
        print("Wrong Algorithm Name")

if __name__ == "__main__":

    #algo = "sat"
    algo = "appsat"
    #algo = "sweep"
    #algo = "sarlock"
    #algo = "rll"
    #algo = "libar"
    #algo = "antisat"
    #algo = "asob"
    org_ckt_ls = "bench_ckt/c432.bench"
    obs_ckt_ls = "obfuscated/c432_rll.bench"
    #obs_ckt_ls = "obfuscated/c432_libar_unrolled.bench"
    key_str = "101111011001100"
    libar_percent = 0.3
    lock_unlock(algo,org_ckt_ls,obs_ckt_ls,key_str,libar_percent)
    print("key= 10011000111110101001100011111010")
    #convert CKT
    #algo_methods.convert_bench2verilog("obfuscated/c432_libar.bench")
    

    

