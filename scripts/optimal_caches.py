from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# All possible L1 caches, LRU
#il1 = ["il1:%s:%s:%s:l" %(x,(y*8),z) for x in [256,512,1024,2048,4096,8192] for y in [1,2,4,8,16] for z in [1,2,4]]
#dl1 = ["dl1:%s:%s:%s:l" %(x,(y*8),z) for x in [256,512,1024,2048,4096,8192] for y in [1,2,4,8,16] for z in [1,2,4]]

# bad: 8192
# not good: 4-way
# good: 2-way, 1-way

# int - not good: 16 ifqsize
# fp - not good: 2 ifqsize

# After reviewing initial L1 results
il1 = ["il1:%s:%s:%s:l" %(x,(y*8),z) for x in [256,512,1024,2048,4096] for y in [2,4,8,16] for z in [1,2]]
#dl1 = ["dl1:%s:%s:%s:l" %(x,(y*8),z) for x in [256,512,1024,2048,4096] for y in [2,4,8,16] for z in [1,2]]

# All possible L2 caches, LRU
#ul2 = ["ul2:%s:%s:%s:l" %(x,(y*8),z) for x in [256,512,1024,2048,4096,8192,16384,32768,65536] for y in [2,4,8,16] for z in [1,2,4,8,16]]

# bad: 65536, 32768; 16-way, 8-way; 16 block (int)
# not good: 16384
# okay: 4-way
# good: 8192, 4096, 2048, 1024, 512, 256; 2-way, 1-way; 32, 64, 128 block; 16 block (float)

# After reviewing initial L2 results
ul2 = ["ul2:%s:%s:%s:l" %(x,(y*8),z) for x in [256,512,1024,2048,4096,8192,16384] for y in [2,4,8,16] for z in [1,2,4]]

makeConfigs("optimal_caches",
	{
		'fetch:ifqsize': [2,4,8,16], # Only certain that ifqsize > 1
		'cache:il1': il1,
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
#runBenchmarksOnTestSets(["optimal_caches"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["optimal_caches"])
