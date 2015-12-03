import fileinput
import os.path
import re
import subprocess
import os



# function:
#	This method will return all the subfolder and subfolder of the subfolder in a list
#
# example:
#	suppose that the result folder has the following structure
#		../results/
#			testSet1/
#				baseline/
#				bzip2/
#			testSet2/
#				baseline/
#				bzip2/
#	running the method will return a list that has the following values
#		result = [["testSet1",["baseline","bzip2"]],["testSet2",["baseline","bzip2"]]			
def getSetsAndTestCases(rootFolderName):
	# get the name of the sets and test cases in the root folder
	Sets = []
	for index,(subdir,dirs,files) in enumerate(os.walk("../%s/" %rootFolderName)):
		if index == 0:
			for i,folder in enumerate(dirs):
				Sets.append([])
				Sets[i].append(folder)

				for j,(subdir2,dirs2,files2) in enumerate(os.walk("../%s/%s" %(rootFolderName,folder))):
					if j == 0:
						Sets[i].append(dirs2)
	return Sets


# function: 
#	This method will through through all the experiment sets under the configs folder 
# 	run the simpleScalar simulation on all the test cases of the sets. The results of the simulation
#	will be placed under the following directory "./results/{experient_set}/{test_case}/"
#
# Important assumption: 
#	if there existing files in a test case of a set ("./results/{experient_set}/{test_case}/"),
#	then the function will not perform the simulation. This is because we are making the assumption that when we are 
#	changing the spreadsheet file, we will not be changing the parameters of a previous test case. If we are going to
#	make any modifications to the spreadsheet, it would make sense that we would only add another testcase
#
#	This assumption allows us to cut down the time that it will take to run through all the test sets
def runBenchmarksOnTestSets():
	# get the name of all the test cases in the results folder
	testSets = getSetsAndTestCases("configs")

	
	for testSet in testSets:
		# check if the  directory for the test set already exist. 
		# skip if it already exists
		# create new directory if not
		if not(os.path.isdir("../results/%s" %testSet[0])):
			os.makedirs("../results/%s" %testSet[0])

		# Loop through all the test cases in the current test set
		for testCase in testSet[1]:

			# check if the  directory for the test case already exist. 
			# skip if it already exists
			# create new directory if not
			if not(os.path.isdir("../results/%s/%s" %(testSet[0],testCase))):
				os.makedirs("../results/%s/%s" %(testSet[0],testCase))

			# check if the directory for the current test case already has output files or not
			#	if it already has files then we will not perform the simultion on this test case
			#	this allows us to shorted the time between execution
			for index,(subdir,dirs,files) in enumerate(os.walk("../results/%s/%s" %(testSet[0],testCase))):
				# only perform the simulation if the test case folder has no files in it
				if not files:
					subprocess.call("./run_experiment.sh %s/%s" %(testSet[0],testCase),
						shell=True)
				




# Function: 
#	This function will loop through all the folders in the /results/ folder and pull the desired data from each 
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
	testSets = getSetsAndTestCases("results")

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



def main():
	parseCSVIntoConfigs()
	runBenchmarksOnTestSets()
	extractDataFromResults(["sim_IPC"])


if __name__ == "__main__":
    main()