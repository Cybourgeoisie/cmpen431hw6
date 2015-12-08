from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

il1 = ["il1:%s:%s:%s:l" %(x,(y*8),z) for x in [1024,2048,4096,8192] for y in [4,8,16] for z in [1,2,4]]

makeConfigs("optimal_cache_L1", 
	{
		'fetch:ifqsize': [4,8,16], # Only certain that ifqsize > 1,2
		'cache:il1': il1,
		'cache:dl2': ["ul2:1024:128:2:l"]
	},
	{
		'bpred': 'comb',    # Certain
		'bpred:ras': 8,     # Only certain that RAS > 0
		'fetch:speed': 2    # Minimal impact
	},
	useOptimal = True
)

# Run tests
#runBenchmarksOnTestSets(["optimal_cache_L1"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["optimal_cache_L1"])
