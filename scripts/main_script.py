import fileinput
import os.path
import re
import subprocess
import os

# Note: you might need to comment out these library and the methods to generate the graphs if you
# can't get python to run 
import matplotlib.pyplot as plt
import pandas as pd 
import ggplot
import numpy as np


# Purpose: This function will loop through all the folders in the /results/ folder and pull the desired data from each 
#	of the benchmarks' output. 
#	The resulting file will be placed under the /results/ folder under the name "results.csv". 
#
# Input: The function takes a list that has the list of parameters that the function will need to pull from the benchmarks. 
#
# Example: extractDataFromResults(["sim_IPC","ifq_latency"])
#	will pull all the "sim_IPC" and "ifq_latency" results from all the benchmarks and place it in a single results.cvs file
#
# Note: if a results.csv file already exits in the ../results/ folder then the function will overwrite the previous file. 

def extractDataFromResults(ListOfParaToGet):
	# get the name of all the test cases in the results folder
	testSets = []
	for index,(subdir,dirs,files) in enumerate(os.walk("../results/")):
		if index == 0:
			for i,folder in enumerate(dirs):
				testSets.append([])
				testSets[i].append(folder)

				for j,(subdir2,dirs2,files2) in enumerate(os.walk("../results/%s" %folder)):
					if j == 0:
						testSets[i].append(dirs2)


	# check if the  directory for the test case already exist. 
	# skip if it already exists
	# create new directory if not
	for testSet in testSets:
		if not(os.path.isdir("../tables/%s" %testSet[0])):
			os.makedirs("../tables/%s" %testSet[0])

		# open the results file in the result folder.
		# Note: this will overwrite the previous value in the result file if the file already exists
		with open("../tables/%s/rawTable.csv" %testSet[0],"w") as f:

			# write the header row
			f.write("testcases,benchmarks")
			for item in ListOfParaToGet:
				f.write(",%s" %item)
			f.write(",clock cycle (ps)\n")

			# Note: the order of this list matters. The first 3 will be the interger benchmarks and the last 2 will be the 
			#	floating point benchmarks
			benchmarks = ["bzip2","hmmer","mcf","sjeng","milc","equake"]

			# now we have to loop through all the folder in the test set and pull the results out
			for folder in testSet[1]:

				# go through all the benchmarks on each of the folder
				for benchmark in benchmarks:
					f.write("%s,%s" %(folder,benchmark))

					# variables for determining clock cycle
					static = True
					issueWidth = 1

					# go though all the lines in the benchmark output and put all the results that matches the parameter that we want
					for line in fileinput.input("../results/%s/%s/%s.out" %(testSet[0],folder,benchmark), inplace=0 , backup=0):
						for parameter in ListOfParaToGet:
							# if the line matches the parameter that we want then extract the numberical value
							if re.match("%s\s+.+" %parameter,line):
								# once the line is split, the result that we want is index 1 of the list
								f.write(",%s" %re.split("\s+",line)[1])

						# pull the value of the issue:inorder and issue:width to determine the clock cycle
						if re.match("(?:(-issue:inorder)|(-issue:width))",line):
							splitLine = re.split("\s+",line)
							if splitLine[0] == "-issue:inorder":
								if splitLine[1] == "false":
									static = False 
							else:
								issueWidth = int(splitLine[1])

					# use the value of static and issueWidth to determine the clock cycle
					if static == True:
						if issueWidth == 1:
							f.write(",100")
						elif issueWidth == 2:
							f.write(",115")
						elif issueWidth == 3:
							f.write(",130")
						elif issueWidth == 4:
							f.write(",145")
						else:
							raise EnvironmentError("Invalid machine issue:width")
					else:
						if issueWidth == 2:
							f.write(",125")
						elif issueWidth == 4:
							f.write(",160")
						elif issueWidth == 8:
							f.write(",195")
						else:
							raise EnvironmentError("Invalid machine issue:width")

					# we are done with a single benchmark so we need to move to a new line
					f.write("\n")
		f.close()


# This function will go though all the test cases that are in the cvs file and create a config file and folder
# 	for each of the test cases. 
# Important assumption: if the folder for the test case already exists then the function will assume that the config file is already 
# 	there and is correct; therefore, it will not try to update that particular test case
def parseCSVIntoConfigs():
	# get the name of all the test sets in the csv folder
	testSetNames = []
	for index,(subdir,dirs,files) in enumerate(os.walk("../csv/")):
		if index == 0:
			testSetNames = dirs

	for testSet in testSetNames:
		# this list contains the name of the test cases that we are trying to do
		testTitle = []
		# this list contains the paremters that we are trying to do
		# for example, ["-bpred:ras","0"] tells use that we need to change the -bpred:ras parameter to 0
		testParameters = []
		baseline = []


		# <-- Opening the csv file and update testTitle and testParameters --->
		f = open("../csv/%s/%s.csv" %(testSet,testSet))
		i = 0
		for line in f:
			data = re.split(r',',line.strip("\r\n"))
			if data[0] == "test":
				testTitle.append(data[1])
				testParameters.append([])
				i = i+ 1
			# Now we need to add all the parameters that we need to change to the testParemeters list
			else:
				testParameters[i-1].append(data) 
		
		#copying data to baseline variable and delete baseline from the previous list so we don't have a duplicate baseline
		baseline = testParameters[0]
		del testParameters[0]


		for index,title in enumerate(testTitle):
			# check if the config file for the test case already exist. 
			# skip if it already exists
			if (os.path.isdir("../configs/%s/%s" %(testSet,title))):
				continue
			else:
				os.makedirs("../configs/%s/%s" %(testSet,title))

			# write all the baseline cases 
			with open("../configs/%s/%s/config.cfg" %(testSet,title),"w") as configFile:
				for parameter in baseline:
					configFile.write("-%s %s\n" %(parameter[0],parameter[1]))

			# only search and replace stuff if this is not the baseline config file
			if index != 0:
				# Now go through and replace all the parameters that we need
				for line in fileinput.input("../configs/%s/%s/config.cfg" %(testSet,title),inplace=1,backup=0):
					for parameter in testParameters[index-1]:
						# This is the pattern that we need to match
						pattern = re.compile("-%s\s.+" %parameter[0])
						if pattern.match(line):
							line = pattern.sub("-%s %s\n" %(parameter[0],parameter[1]),line)
					print (line.strip("\n"))



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

		geometricMeanDF.to_csv("../graphs/%s/%s_Table" %(table,table))
		geometricMeanDF.plot(kind="line")
		plt.title(table)
		plt.xlabel("Benchmarks")
		plt.ylabel("Execution Time (ms)")
		plt.savefig("../graphs/%s/%s_Graph" %(table,table))




def main():
	parseCSVIntoConfigs()
	extractDataFromResults(["sim_IPC"])
	generateGraphs()


if __name__ == "__main__":
    main()