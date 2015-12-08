from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# All possible L1 caches, LRU
#il1 = ["il1:%s:%s:%s:l" %(x,(y*8),z) for x in [256,512,1024,2048,4096,8192] for y in [1,2,4,8,16] for z in [1,2,4]]
#dl1 = ["dl1:%s:%s:%s:l" %(x,(y*8),z) for x in [256,512,1024,2048,4096,8192] for y in [1,2,4,8,16] for z in [1,2,4]]

# All possible L2 caches, LRU
ul2 = ["ul2:%s:%s:%s:l" %(x,(y*8),z) for x in [256,512,1024,2048,4096,8192,16384,32768,65536] for y in [2,4,8,16] for z in [1,2,4,8,16]]

makeConfigs("optimal_L2_cache", 
	{
		#'fetch:ifqsize': [2,4,8,16], # Only certain that ifqsize > 1
		#'cache:il1': il1,
		#'cache:dl1': dl1,
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
#runBenchmarksOnTestSets(["optimal_L2_cache"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["optimal_L2_cache"])
