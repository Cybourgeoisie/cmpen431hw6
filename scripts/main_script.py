import fileinput
import os.path
import re
import subprocess
import os


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
	testCasesName = []
	for index,(subdir,dirs,files) in enumerate(os.walk("../results/")):
		if index == 0:
			testCasesName = dirs


	# open the results file in the result folder.
	# Note: this will overwrite the previous value in the result file if the file already exists
	with open("../results/results.cvs","w") as f:

		# write the header row
		f.write("testcases,benchmarks")
		for item in ListOfParaToGet:
			f.write(",%s" %item)
		f.write(",clock cycle (ps)\n")

		benchmarks = ["bzip2","equake","hmmer","mcf","milc","sjeng"]

		# now we have to loop through all the folder and pull the results out
		for folder in testCasesName:

			# go through all the benchmarks on each of the folder
			for benchmark in benchmarks:
				f.write("%s,%s" %(folder,benchmark))

				# variables for determining clock cycle
				static = True
				issueWidth = 1

				# go though all the lines in the benchmark output and put all the results that matches the parameter that we want
				for line in fileinput.input("../results/%s/%s.out" %(folder,benchmark), inplace=0 , backup=0):
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
def parseCSVIntoConfigs(csvFileName):
	# this list contains the name of the test cases that we are trying to do
	testTitle = []
	# this list contains the paremters that we are trying to do
	# for example, ["-bpred:ras","0"] tells use that we need to change the -bpred:ras parameter to 0
	testParameters = []
	baseline = []


	# <-- Opening the csv file and update testTitle and testParameters --->
	f = open("../csv/%s.csv" %csvFileName)
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
	
	#copying data to baseline variable and delete from the previous list so we don't have a duplicate baseline
	baseline = testParameters[0]
	del testParameters[0]
	del testTitle[0]

	for index,title in enumerate(testTitle):
		# check if the config file for the test case already exist. 
		# skip if it already exist`s
		if (os.path.isdir("../configs/%s" %title)):
			continue
		else:
			os.makedirs("../configs/%s" %title)

		# write all the baseline cases 
		with open("../configs/%s/%s" %(title,title),"w") as configFile:
			for parameter in baseline:
				configFile.write("%s %s\n" %(parameter[0],parameter[1]))

		# Now go through and replace all the parameters that we need
		for line in fileinput.input("../configs/%s/%s" %(title,title),inplace=1,backup=0):
			for parameter in testParameters[index]:
				# This is the pattern that we need to match
				pattern = re.compile("%s\s.+" %parameter[0])
				if pattern.match(line):
					line = pattern.sub("%s %s\n" %(parameter[0],parameter[1]),line)
			print (line.strip("\n"))



def main():
	parseCSVIntoConfigs("testcases")


if __name__ == "__main__":
    main()