from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults


# il1 and dl1 cache block size are fixed at ifqize * 8
il1 = ["il1:%s:%s:1:l" %(int(1024/x),x*8) for x in [1,2,4,8,16]]
dl1 = ["dl1:%s:%s:1:l" %(int(1024/x),x*8) for x in [1,2,4,8,16]]


makeConfigs("ex_ifq_speed_decode", 
	{'fetch:ifqsize': [1,2,4,8,16], 'fetch:speed': range(1,5), 'decode:width': [1,2,4,8,16],
	 'cache:il1': il1,
	 'cache:dl1': dl1
	 },
	{}
)

# Run tests
runBenchmarksOnTestSets(["ex_ifq_speed_decode"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["ex_ifq_speed_decode"])
