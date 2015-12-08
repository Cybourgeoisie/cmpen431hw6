from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# il1 and dl1 cache block size are fixed at ifqize * 8
il1 = ["il1:1024:%s:1:l" %(x*8) for x in [4,8,16]]

dl2 = ["dl2:%s:16:1:l" %(x) for x in [4096,8192,16384,32768,65536]]

makeConfigs("optimal_w_bpred_test_ifqsize_fetch_speed", 
	{
		#'fetch:ifqsize': [4,8,16],
		#'fetch:speed': [1,4],
		'cache:il1': il1,
		'cache:dl2': dl2
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
