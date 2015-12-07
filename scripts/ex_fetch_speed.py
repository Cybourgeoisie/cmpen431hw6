from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

makeConfigs("fetch_speed", 
	{'fetch:speed': range(1,5)},
	{}
)

# Run tests
#runBenchmarksOnTestSets(["fetch_speed"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["fetch_speed"])
