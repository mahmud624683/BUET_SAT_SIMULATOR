import algo_methods
import argparse
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

parser = argparse.ArgumentParser(description='algo_methods implementation with MonoSAT')
#parser.add_argument("--algorithm", action="store", required=True, type=str, default="sat", help="sat/appsat/sweep")
parser.add_argument("--original", action="store", required=True, type=str, default=" ", help="original benchmark path")
parser.add_argument("--obfuscated", action="store", required=True, type=str, default=" ", help="obfuscated benchmark path")
#parser.add_argument("--repeats", action="store", required=True, type=int, default=0, help="number of attack repeats")

args = parser.parse_args()

dum_org = "../../Tanveer/c17_dum.bench"
dum_obs = "../../Tanveer/c17_as.bench"

#attack_count=0

#while(attack_count<=args.repeats):
logging.info("Running SAT algorithm...")
print(algo_methods.sat(args.original, args.obfuscated))
logging.info("Running APPSAT algorithm...")
print(algo_methods.appsat(args.original, args.obfuscated))
logging.info("Running Hamming Sweep algorithm...")
print(algo_methods.hamming_sweep(args.original, args.obfuscated))
logging.info("Refreshing Memory after Sweep using SAS...")
algo_methods.sat(dum_org, dum_obs)
algo_methods.appsat(dum_org, dum_obs)
algo_methods.sat(dum_org, dum_obs)
logging.info("Memory Refreshed...")