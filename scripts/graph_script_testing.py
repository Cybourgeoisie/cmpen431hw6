import matplotlib.pyplot as plt
import pandas as pd 
import ggplot
import numpy as np



def reportFromDataFrame(inputDataFrame,paraToPlot):
	newDataFrame = pd.DataFrame()
	# Each test cases has 6 benchmarks so if we divide the length of the dataframe
	#	by 6 then we will be left with the number of test cases. This will allow us
	#	to slice to dataFrame to get the testcase that we want 
	for i in range(1,len(inputDataFrame.index)/6+1):
		# if i == 1, then we will need to set the index for our new dataframe
		if i == 1:
			newDataFrame["benchmarks"] = inputDataFrame[:i*6]["benchmarks"]
		# Slice the dataFrame to get the testcase that we want
		offsetDataFrame = inputDataFrame[(i-1)*6:i*6]
		# insert the testcase into the newDataFrame
		offsetDataFrame.index = range(0,6)
		newDataFrame[inputDataFrame.loc[(i-1)*6,"testcases"]] = offsetDataFrame["sim_IPC"]
	# Change the index of the newdataframe
	newDataFrame = newDataFrame.set_index("benchmarks")

	newDataFrame.to_csv("../results/%sTable" %paraToPlot)
	newDataFrame.plot(kind="line")
	plt.xlabel("Benchmarks")
	plt.ylabel(paraToPlot)
	plt.savefig("../results/%sGraph" %paraToPlot)

def main():
	data = pd.read_csv("../results/results.csv")
	reportFromDataFrame(data,"sim_IPC")

if __name__ == "__main__":
    main()



