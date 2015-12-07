from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# Test how the integer ALU / mult affect geometric means
makeConfigs("ialu_imult_memport", 
	{'res:ialu': range(1,9), 'res:imult': range(1,9), 'res:memport': [1,2]},
	{}
)

# Run tests
#runBenchmarksOnTestSets(["ialu_imult_memport"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["ialu_imult_memport"])
