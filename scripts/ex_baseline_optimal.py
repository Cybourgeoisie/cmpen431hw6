from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# Calculate the baseline
makeConfigs("baseline_optimal", 
	{},
	{},
	useOptimal = True
)

# Run tests
#runBenchmarksOnTestSets(["baseline_optimal"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["baseline_optimal"])
