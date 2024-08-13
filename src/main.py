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
    else:
        print("Wrong Algorithm Name")

if __name__ == "__main__":

    algo = "sat"
    #algo = "appsat"
    #algo = "sweep"
    #algo = "sarlock"
    #algo = "rll"
    #algo = "libar"
    org_ckt_ls = "benchmarks/originals/c432.bench"
    #obs_ckt_ls = "benchmarks/Mahmudul Circuits/c432_libar.bench"
    obs_ckt_ls = "benchmarks/Mahmudul Circuits/c432_libar_unrolled.bench"
    key_str = "0101110000110111110000101010"
    libar_percent = 0.01
    lock_unlock(algo,org_ckt_ls,obs_ckt_ls,key_str,libar_percent)

    #convert CKT
    #converts.bench2verilog(file_path = "benchmarks/originals/c17.bench", file_name="c17")

    

