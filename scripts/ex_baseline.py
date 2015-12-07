from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# Calculate the baseline
makeConfigs("baseline", 
	{},
	{}
)

# Run tests
runBenchmarksOnTestSets(["baseline"])

# Retrieve results
extractDataFromResults(["sim_IPC"], ["baseline"])
