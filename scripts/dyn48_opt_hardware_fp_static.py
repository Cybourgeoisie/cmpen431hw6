from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# int, followed by fp:
#il1 = ["il1:256:64:2:l", "il1:512:64:1:l"]
il1 = ["il1:256:64:2:l"]

# same for int & fp:
#ul2 = ["ul2:2048:128:4:l", "ul2:4096:128:2:l"]
# winner by a hair for both int and fp
ul2 = ["ul2:4096:128:2:l"]

# fp:
fetchspeed = [3,4]
# int:
fetchspeed = [1,2,3,4]

makeConfigs("dyn48_opt_hardware_fp_static",
	{
		'cache:il1':   il1,
		'cache:dl2':   ul2,
		#'fetch:speed': fetchspeed,
		'res:fpalu':   2,
		'res:fpmult':  2,
		'res:ialu':    range(2,9),
		'res:imult':   range(1,9),
	},
	{
		'res:memport': 2,   # Safe assumption? To be tested
		'fetch:ifqsize': 8, # Near certain
		'fetch:speed': 3,   # To be tested
		'bpred': 'comb',    # Certain
		'bpred:ras': 8,     # To be tested
	},
	{
		'static'  : [],
		'dynamic' : [4,8]
	},
	useOptimal = True
)

# Run tests
#runBenchmarksOnTestSets(["dyn48_opt_hardware_fp_static"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["dyn48_opt_hardware_fp_static"])
