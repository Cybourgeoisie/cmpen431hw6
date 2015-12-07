from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# Test how the integer ALU / mult affect geometric means
makeConfigs("fpalu_fpmult_memport", 
	{'res:fpalu': range(1,9), 'res:fpmult': range(1,9), 'res:memport': [1,2]},
	{}
)

# Run tests
#runBenchmarksOnTestSets(["fpalu_fpmult_memport"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["fpalu_fpmult_memport"])
