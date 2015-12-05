from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# Create configs for ialu / imult test
makeConfigs("ialu_imult_test", 
	{'res:ialu': range(1,15), 'res:imult': range(1,15)},
	{}
)

# Run tests on ialu and imult
runBenchmarksOnTestSets(["ialu_imult_test"])

# Collect all of the results
extractDataFromResults(["sim_IPC"], ["ialu_imult_test"])
