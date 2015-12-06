import fileinput
import os.path
import re
import subprocess
import os

import matplotlib.pyplot as plt
import pandas as pd 
import ggplot
import numpy as np



# this function will return a tuple oft dataframes
#	1st tuple = the DF with both the interger and floating point GM
#	2nd tuple = the DF with the interger GM sorted in descending order
#	3rd tuple = the DF with the floating point GM sorted in descending order
def calculateGeometricMeans(inputDataFrame):

	# DF with both interger and floating point
	GeoMeansDF = pd.DataFrame()
	GeoMeansDF["benchmarks"] = ["integer","floating point"]

	# DF with interger 
	GeoMeansDF_int = pd.DataFrame()
	GeoMeansDF_int["benchmarks"] = ["execution time (ms)"]

	# DF with both interger and floating point
	GeoMeansDF_float = pd.DataFrame()
	GeoMeansDF_float["benchmarks"] = ["execution time (ms)"]

	# execution time = [2500000 x clock cycle (ps)] / sim_IPC
	inputDataFrame["execution time (ms)"] = ((inputDataFrame["clock cycle (ps)"] * pow(10,-9)) * 2500000) / inputDataFrame["sim_IPC"]

	# Each test cases has 6 benchmarks so if we divide the length of the dataframe
	#	by 6 then we will be left with the number of test cases. This will allow us
	#	to slice to dataFrame to get the testcase that we want 
	for i in range(1,len(inputDataFrame.index)/6+1):
		# initialized variables for our geometric means
		integerGM = 0
		floatingGM = 0
		# Slice the dataFrame to get the testcase that we want
		offsetDataFrame = inputDataFrame[(i-1)*6:i*6]
		# Change the index of the offset DF
		offsetDataFrame.index = range(0,6)

		# take the product of all the exectiontime for the integer execution time
		for index,intExeTime in enumerate(offsetDataFrame[:4]["execution time (ms)"]):
			if index == 0:
				integerGM = intExeTime
			else:
				integerGM *= intExeTime

		# take the product of all the exectiontime for the floating point execution time
		for index,floatExeTime in enumerate(offsetDataFrame[4:6]["execution time (ms)"]):
			if index == 0:
				floatingGM = floatExeTime
			else:
				floatingGM *= floatExeTime

		integerGM = pow(integerGM,1.0/4.0)
		floatingGM = pow(floatingGM,1.0/2.0)
		testName = inputDataFrame.loc[(i-1)*6,"testcases"]

		# attached the new geometric means to the dataframe
		GeoMeansDF[testName] = [integerGM,floatingGM]
		GeoMeansDF_float[testName] = [floatingGM]
		GeoMeansDF_int[testName] = [integerGM]


	GeoMeansDF = GeoMeansDF.set_index("benchmarks")
	GeoMeansDF_int = GeoMeansDF_int.set_index("benchmarks")
	GeoMeansDF_float = GeoMeansDF_float.set_index("benchmarks")

	GeoMeansDF_int = GeoMeansDF_int.T.sort_values('execution time (ms)',ascending=[0])
	GeoMeansDF_float = GeoMeansDF_float.T.sort_values('execution time (ms)',ascending=[0])

	return (GeoMeansDF,GeoMeansDF_int,GeoMeansDF_float)


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

		geometricMeanDFTuple = calculateGeometricMeans(DF)

		geometricMeanDFTuple[0].to_csv("../graphs/%s/%s_Table.csv" %(table,table))
		
		# generate the tables and graph for the interger and floating point benchmarks
		for i in [1,2]:
			benchmarkType = "int" if(i == 1) else "floating"
			resultDF = geometricMeanDFTuple[i]

			resultDF.to_csv("../graphs/%s/%s_%s_Table.csv" %(table,table,benchmarkType))

			# only plot the first 10 benchmarks with the highest execution time
			resultDF[:10].plot(kind="line")
			plt.title("%s_%s" %(table,benchmarkType))
			plt.xlabel("Test Cases",size=5)
			plt.xticks(rotation=70)
			plt.ylabel("Execution Time (ms)",size=10)
			plt.legend(prop={'size':8})
			plt.tight_layout(pad=.2,)
			plt.savefig("../graphs/%s/%s_%s_Graph.jpeg" %(table,table,benchmarkType),dpi=300)

		


def main():
	generateGraphs()


if __name__ == "__main__":
    main()