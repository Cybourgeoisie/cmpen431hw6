from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# int, followed by fp:
il1 = ["il1:256:64:2:l", "il1:512:64:1:l"]

# same for int & fp:
#ul2 = ["ul2:2048:128:4:l", "ul2:4096:128:2:l"]
# winner by a hair for both int and fp
ul2 = ["ul2:4096:128:2:l"]

# fp:
fetchspeed = [3,4]
# int:
fetchspeed = [1,2,3,4]

makeConfigs("dyn2_int_opt_hardware",
	{
		'cache:il1':   il1,
		'cache:dl2':   ul2,
		#'fetch:speed': fetchspeed,
		'res:fpalu':   range(1,9),
		'res:fpmult':  range(1,9),
		'res:memport': [1,2],
		'res:ialu':    range(1,9),
		'res:imult':   range(1,9),
	},
	{
		'fetch:ifqsize': 8,
		'fetch:speed': 3,
		'bpred': 'comb',    # Certain
		'bpred:ras': 8,     # Only certain that RAS > 0
	},
	{
		'static'  : [],
		'dynamic' : [2]
	},
	useOptimal = True
)

# Run tests
#runBenchmarksOnTestSets(["dyn2_int_opt_hardware"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["dyn2_int_opt_hardware"])
