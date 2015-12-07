from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

makeConfigs("ruu_lsq", 
	{'ruu:size': [4,8,16,32,64], 'lsq:size': [2,4,8,16,32]},
	{},
	{'static': [], 'dynamic': [2,4,8]}
)

# Run tests
#runBenchmarksOnTestSets(["ruu_lsq"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["ruu_lsq"])
