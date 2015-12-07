from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# Calculate the baseline
makeConfigs("baseline_optimal_bpred_ras", 
	{'bpred': ['2lev', 'comb', 'bimod'], 'bpred:ras': [8,16]},
	{},
	useOptimal = True
)

# Run tests
#runBenchmarksOnTestSets(["baseline_optimal_bpred_ras"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["baseline_optimal_bpred_ras"])
