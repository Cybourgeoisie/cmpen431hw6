from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# Collect all of the results
extractDataFromResults(["sim_IPC"], ["ialu_imult_test"])
