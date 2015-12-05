from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# Create configs for fpalu / fpmult test
makeConfigs("fpalu_fpmult_test", 
	{'res:fpalu': range(1,8), 'res:fpmult': range(1,8)},
	{}
)

# Run tests on fpalu and fpmult
runBenchmarksOnTestSets(["fpalu_fpmult_test"])

# Collect all of the results
extractDataFromResults(["sim_IPC"], ["fpalu_fpmult_test"])
