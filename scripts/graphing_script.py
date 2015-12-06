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
	GeoMeansDF["benchmarks"] = ["integer","floating point"]

	# Get the baseline runtimes
	# int baseline,bzip2, 0.1992,100
	# int baseline,hmmer, 0.4625,100
	# int baseline,mcf,   0.3186,100
	# int baseline,sjeng, 0.2684,100
	# fp  baseline,milc,  0.4234,100
	# fp  baseline,equake,0.2696,100
	integerGMBaseline  =  100 * 2500000 / 0.1992 * pow(10,-6)
	integerGMBaseline  *= 100 * 2500000 / 0.4625 * pow(10,-6)
	integerGMBaseline  *= 100 * 2500000 / 0.3186 * pow(10,-6)
	integerGMBaseline  *= 100 * 2500000 / 0.2684 * pow(10,-6)
	floatingGMBaseline =  100 * 2500000 / 0.4234 * pow(10,-6)
	floatingGMBaseline *= 100 * 2500000 / 0.2696 * pow(10,-6)

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
		integerGM = 1
		for index,intExeTime in enumerate(offsetDataFrame[:4]["execution time (us)"]):
			integerGM *= intExeTime
		integerGM /= integerGMBaseline

		# take the product of all the exectiontime for the floating point execution time
		floatingGM = 1
		for index,floatExeTime in enumerate(offsetDataFrame[4:6]["execution time (us)"]):
			floatingGM *= floatExeTime
		floatingGM /= floatingGMBaseline

		# attached the new geometric means to the dataframe
		GeoMeansDF[inputDataFrame.loc[(i-1)*6,"testcases"]] = [pow(integerGM,1.0/4.0),pow(floatingGM,1.0/2.0)]

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
		plt.xlabel("Benchmarks",size=10)
		plt.ylabel("Execution Time (us)",size=10)
		plt.legend(prop={'size':8})

		plt.savefig("../graphs/%s/%s_Graph.jpeg" %(table,table),dpi=300)


def main():
	generateGraphs()


if __name__ == "__main__":
    main()