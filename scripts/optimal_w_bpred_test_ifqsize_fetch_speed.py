from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# il1 and dl1 cache block size are fixed at ifqize * 8
il1 = ["il1:%s:%s:1:l" %(int(1024/x),x*8) for x in [4,8,16]]

makeConfigs("optimal_w_bpred_test_ifqsize_fetch_speed", 
	{
		'fetch:ifqsize': [4,8,16],
		'fetch:speed': [1,4],
		'cache:il1': il1
	},
	{
		'bpred': 'comb', # Certain
		'bpred:ras': 8,  # Only certain that RAS > 0
	},
	useOptimal = True
)

# Run tests
#runBenchmarksOnTestSets(["optimal_w_bpred_test_ifqsize_fetch_speed"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["optimal_w_bpred_test_ifqsize_fetch_speed"])
