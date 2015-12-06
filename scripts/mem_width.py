import sys
sys.path.append('../')

from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# Test how the mem:width affect geometric means
makeConfigs("mem_width", 
	{'mem:width': [8,16]},
	{}
)


# Run tests
#runBenchmarksOnTestSets(["mem_width"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["mem_width"])
