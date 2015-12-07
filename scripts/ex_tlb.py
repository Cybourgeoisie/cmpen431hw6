from make_configs import makeConfigs
from main_script import runBenchmarksOnTestSets, extractDataFromResults

# ['itlb:256:4096:1:l', 'itlb:128:4096:2:l', 'itlb:64:4096:4:l', 'itlb:32:4096:8:l', 'itlb:16:4096:16:l', 'itlb:8:4096:32:l', 'itlb:4:4096:64:l', 'itlb:2:4096:128:l', 'itlb:1:4096:256:l']
itlb = ["itlb:%s:4096:%s:l" %(int(256/(2**x)), 2**x) for x  in range(0,9) ] 

# ['dtlb:512:4096:1:l', 'dtlb:256:4096:2:l', 'dtlb:128:4096:4:l', 'dtlb:64:4096:8:l', 'dtlb:32:4096:16:l', 'dtlb:16:4096:32:l', 'dtlb:8:4096:64:l', 'dtlb:4:4096:128:l', 'dtlb:2:4096:256:l', 'dtlb:1:4096:512:l']
dtlb = ["dtlb:%s:4096:%s:l" %(int(512/(2**x)), 2**x) for x  in range(0,10) ]


makeConfigs("ex_tlb", 
	{ 'tlb:itlb': itlb, 'tlb:dtlb': dtlb },
	{}
)

# Run tests
runBenchmarksOnTestSets(["ex_tlb"])

# Retrieve results
# extractDataFromResults(["sim_IPC"], ["ex_tlb"])
