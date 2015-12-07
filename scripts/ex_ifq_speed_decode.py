from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

makeConfigs("ifq_speed_decode", 
	{'fetch:ifqsize': [1,2,4,8,16], 'fetch:speed': range(1,5), 'decode:width': [1,2,4,8,16],
	 'cache:il1': ['il1:512:8:1:r', 'il1:512:16:1:r', 'il1:512:32:1:r', 'il1:512:64:1:r', 'il1:512:128:1:r'],
	 'cache:dl1': ['dl1:512:8:1:r', 'dl1:512:16:1:r', 'dl1:512:32:1:r', 'dl1:512:64:1:r', 'dl1:512:128:1:r']
	 },
	{}
)

# Run tests
#runBenchmarksOnTestSets(["ifq_speed_decode"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["ifq_speed_decode"])
