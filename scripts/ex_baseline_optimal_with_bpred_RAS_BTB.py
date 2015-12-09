from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

btb = ["%s %s" %(x,y) for y in [1,2,4]for x in [512,1024]]


# Calculate the baseline
makeConfigs("ex_baseline_optimal_with_bpred_RAS_BTB", 
	{'bpred': ['2lev', 'comb', 'bimod'],
	'bpred:ras': range(0,17),
	'bpred:btb': bpred:btb
	},

	{},
	useOptimal = True
)

# Run tests
runBenchmarksOnTestSets(["ex_baseline_optimal_with_bpred_RAS_BTB"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["ex_baseline_optimal_with_bpred_RAS_BTB"])
