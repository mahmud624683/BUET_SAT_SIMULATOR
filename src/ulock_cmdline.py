import algo_methods
import argparse,logging,os

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='BUET SAT SIMULATOR')
    parser.add_argument("--algorithm", action="store", required=True, type=str, default="sweep", help="The selected algorithm (attack)")
    parser.add_argument("--original", action="store", required=True, type=str, default=" ", help="original benchmark path")
    parser.add_argument("--obfuscated", action="store", required=True, type=str, default=" ", help="obfuscated benchmark path")
    
    args = parser.parse_args()


    filename = os.path.basename(args.obfuscated)
    if args.algorithm.lower() == "sat":
	 print(f"{filename} SAT Attack: ")
        result = algo_methods.sat(args.original, args.obfuscated, max_iter=1000, print_str=f"{filename} SAT Attack: ")
        open("src/raw_rslt.txt", 'a').write(result)
        logging.error(result)
    elif args.algorithm.lower() == "appsat":  # dn
        print(f"{filename} SAT Attack: ")
        result = algo_methods.appsat(args.original, args.obfuscated, max_iter=1000, print_str=f"{filename} APPSAT Attack: ")
        open("src/raw_rslt.txt", 'a').write(result)
        logging.error(result)
    elif args.algorithm.lower() == "sweep":  # dn
        print(f"{filename} SAT Attack: ")
        result = algo_methods.hamming_sweep(args.original, args.obfuscated, max_iter=100000, print_str=f"{filename} SWEEP Attack: ")    
        open("src/raw_rslt.txt", 'a').write(result)
        logging.error(result)
    else:
        logging.error("The requested attack/defense algorithm is not defined in the SMT package.")
