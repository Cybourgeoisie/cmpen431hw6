from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# After reviewing initial L1 results
#il1 = ["il1:%s:%s:%s:l" %(x,(y*8),z) for x in [256,512,1024,2048] for y in [4,8] for z in [1,2]]
il1 = ["il1:%s:%s:%s:l" %(x,(y*8),z) for x in [512,1024,2048] for y in [4,8] for z in [1]]

# After reviewing initial L2 results
#ul2 = ["ul2:%s:%s:%s:l" %(x,(y*8),z) for x in [2048,4096,8192] for y in [8,16] for z in [2,4]]
ul2 = ["ul2:%s:%s:%s:l" %(x,(y*8),z) for x in [4096,8192] for y in [8,16] for z in [2,4]]

makeConfigs("dyn2_fp_opt_processor_params",
	{
		'fetch:ifqsize': [4,8], # Only certain that ifqsize > 1
		'cache:il1': il1,
		'cache:dl2': ul2,
		'fetch:speed': [1,2,3,4],
		'decode:width': [1,2,4,8]
	},
	{
		'bpred': 'comb',    # Certain
		'bpred:ras': 8,     # Only certain that RAS > 0
	},
	{
		'static'  : [],
		'dynamic' : [2]
	},
	useOptimal = True
)

# Run tests
#runBenchmarksOnTestSets(["dyn2_fp_opt_processor_params"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["dyn2_fp_opt_processor_params"])
