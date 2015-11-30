import fileinput
import os.path
import re
import subprocess


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