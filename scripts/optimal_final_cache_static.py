from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# After reviewing initial L1 results
il1 = ["il1:%s:%s:%s:l" %(x,(y*8),z) for x in [256,512,1024,2048] for y in [4,8] for z in [1,2]]

# ifqsize = [4,8]
# nsets:
# int: 256, 512, (1024)
# fp:  512, 1024, 2048
# blocks:
# int: 32, 64
# fp: 32, 64
# ways:
# int: (1,) 2
# fp: 1


# After reviewing initial L2 results
ul2 = ["ul2:%s:%s:%s:l" %(x,(y*8),z) for x in [2048,4096,8192] for y in [8,16] for z in [2,4]]

# ifqsize = [4,8,16]
# nsets:
# int: 2048, 4096
# fp:  4096, 8192
# blocks:
# int: 128
# fp: 64, 128
# ways:
# int: 2, 4
# fp: 2, (4)

makeConfigs("optimal_final_cache_static",
	{
		'fetch:ifqsize': [4,8,16], # Only certain that ifqsize > 1
		'cache:il1': il1,
		'cache:dl2': ul2
	},
	{
		'bpred': 'comb',    # Certain
		'bpred:ras': 8,     # Only certain that RAS > 0
		'fetch:speed': 2    # Minimal impact
	},
	{
		'static'  : [1,2,4],
		'dynamic' : []
	},
	useOptimal = True
)

# Run tests
#runBenchmarksOnTestSets(["optimal_final_cache_static"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["optimal_final_cache_static"])
