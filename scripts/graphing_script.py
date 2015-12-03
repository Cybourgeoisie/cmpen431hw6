import fileinput
import os.path
import re
import subprocess
import os

import matplotlib.pyplot as plt
import pandas as pd 
import ggplot
import numpy as np



def calculateGeometricMeans(inputDataFrame):

	GeoMeansDF = pd.DataFrame()
	GeoMeansDF["benchmarks"] = ["interger","floating point"]

	# execution time = [2500000 x clock cycle (ps)] / sim_IPC
	inputDataFrame["execution time (ms)"] = ((inputDataFrame["clock cycle (ps)"] * pow(10,-9)) * 2500000) / inputDataFrame["sim_IPC"]

	# Each test cases has 6 benchmarks so if we divide the length of the dataframe
	#	by 6 then we will be left with the number of test cases. This will allow us
	#	to slice to dataFrame to get the testcase that we want 
	for i in range(1,len(inputDataFrame.index)/6+1):
		# initialized variables for our geometric means
		intergerGM = 0
		floatingGM = 0
		# Slice the dataFrame to get the testcase that we want
		offsetDataFrame = inputDataFrame[(i-1)*6:i*6]
		# Change the index of the offset DF
		offsetDataFrame.index = range(0,6)

		# take the product of all the exectiontime for the interger execution time
		for index,intExeTime in enumerate(offsetDataFrame[:4]["execution time (ms)"]):
			if index == 0:
				intergerGM = intExeTime
			else:
				intergerGM *= intExeTime

		# take the product of all the exectiontime for the floating point execution time
		for index,floatExeTime in enumerate(offsetDataFrame[4:6]["execution time (ms)"]):
			if index == 0:
				floatingGM = floatExeTime
			else:
				floatingGM *= floatExeTime

		# attached the new geometric means to the dataframe
		GeoMeansDF[inputDataFrame.loc[(i-1)*6,"testcases"]] = [pow(intergerGM,1.0/4.0),pow(floatingGM,1.0/2.0)]

	GeoMeansDF = GeoMeansDF.set_index("benchmarks")


	return GeoMeansDF


def generateGraphs():
	# get the name of all the table sets in the table folder
	tableSets = []
	for index,(subdir,dirs,files) in enumerate(os.walk("../tables/")):
		if index == 0:
			tableSets = dirs
	
	# go through all the tables and generate the geomentric means graph for them
	for table in tableSets:

		if not(os.path.isdir("../graphs/%s" %table)):
			os.makedirs("../graphs/%s" %table)

		DF = pd.read_csv("../tables/%s/rawTable.csv" %(table))
		geometricMeanDF = calculateGeometricMeans(DF)

		geometricMeanDF.to_csv("../graphs/%s/%s_Table.csv" %(table,table))
		geometricMeanDF.plot(kind="line")
		plt.title(table)
		plt.xlabel("Benchmarks")
		plt.ylabel("Execution Time (ms)")
		plt.savefig("../graphs/%s/%s_Graph" %(table,table))


def main():
	generateGraphs()


if __name__ == "__main__":
    main()