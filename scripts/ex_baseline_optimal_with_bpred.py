from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# Calculate the baseline
makeConfigs("baseline_optimal_bpred", 
	{'bpred': ['2lev', 'comb', 'bimod']},
	{},
	useOptimal = True
)

# Run tests
#runBenchmarksOnTestSets(["baseline_optimal_bpred"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["baseline_optimal_bpred"])
