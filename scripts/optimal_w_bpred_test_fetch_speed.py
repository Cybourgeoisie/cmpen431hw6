from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# il1 and dl1 cache block size are fixed at ifqize * 8
il1 = ["il1:512:%s:1:l" %(x*8) for x in [8]]

makeConfigs("optimal_w_bpred_test_fetch_speed", 
	{
		'fetch:ifqsize': [8],
		'fetch:speed': [1,2,3,4],
		'cache:il1': il1,
		'cache:dl2': ["ul2:1024:128:2:l"]
	},
	{
		'bpred': 'comb', # Certain
		'bpred:ras': 8,  # Only certain that RAS > 0
	},
	useOptimal = True
)

# Run tests
#runBenchmarksOnTestSets(["optimal_w_bpred_test_fetch_speed"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["optimal_w_bpred_test_fetch_speed"])
