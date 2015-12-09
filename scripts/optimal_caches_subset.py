from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# After reviewing initial L1 results
il1 = ["il1:%s:%s:%s:l" %(x,(y*8),z) for x in [64,128,256,512] for y in [2,4,8,16] for z in [1,2]]

# After reviewing initial L2 results
ul2 = ["ul2:%s:%s:%s:l" %(x,(y*8),z) for x in [1024,2048,4096,8192] for y in [8,16] for z in [1,2,4]]

makeConfigs("optimal_caches_subset",
	{
		'fetch:ifqsize': [2,4,8,16], # Only certain that ifqsize > 1
		'cache:il1': il1,
		'cache:dl2': ul2
	},
	{
		'bpred': 'comb',    # Certain
		'bpred:ras': 8,     # Only certain that RAS > 0
		'fetch:speed': 2    # Minimal impact
	},
	{
		'static'  : [],
		'dynamic' : [2]
	},
	useOptimal = True
)

# Run tests
runBenchmarksOnTestSets(["optimal_caches_subset"])

# Retrieve results
extractDataFromResults(["sim_IPC"], ["optimal_caches_subset"])
