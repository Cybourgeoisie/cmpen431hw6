from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# Create configs for fpalu / fpmult test
makeConfigs("fpalu_fpmult_memport2_test", 
	{'res:fpalu': range(1,9), 'res:fpmult': range(1,9)},
	{'res:memport': 2}
)

# Run tests on fpalu and fpmult
runBenchmarksOnTestSets(["fpalu_fpmult_memport2_test"])

# Collect all of the results
extractDataFromResults(["sim_IPC"], ["fpalu_fpmult_memport2_test"])
