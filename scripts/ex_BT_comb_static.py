from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# il1 and dl1 cache block size are fixed at ifqize * 8
il1_1way = ["il1:%s:8:1:l" %x for x in [1024,2048,4096,8192]]
il1_2way = ["il1:%s:8:2:l" %(x/2) for x in [1024,2048,4096,8192]]
il1_4way = ["il1:%s:8:4:l" %(x/4) for x in [1024,2048,4096,8192]]

# ul2 block size must be il1 * 2
dl2_1way = ["dl2:%s:16:1:l" %(x) for x in [4096,8192,16384,32768,65536]]
dl2_2way = ["dl2:%s:16:2:l" %(x/2) for x in [4096,8192,16384,32768,65536]]
dl2_4way = ["dl2:%s:16:4:l" %(x/4) for x in [4096,8192,16384,32768,65536]]
dl2_8way = ["dl2:%s:16:8:l" %(x/8) for x in [4096,8192,16384,32768,65536]]
dl2_16way = ["dl2:%s:16:16:l" %(x/16) for x in [4096,8192,16384,32768,65536]]


makeConfigs("ex_BT_comb_static", 
	{'cache:il1': il1_1way + il1_2way + il1_4way,
	'cache:dl2': dl2_1way + dl2_2way + dl2_4way + dl2_8way + dl2_16way},
	{'bpred': 'comb'},
	{'static': [1,2,4], 'dynamic': []}
)

# Run tests
runBenchmarksOnTestSets(["ex_BT_comb_static"])

# Retrieve results
#extractDataFromResults(["sim_IPC"], ["ex_BT_comb_static"])
