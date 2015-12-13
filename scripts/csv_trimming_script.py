import fileinput
import os.path
import re

import matplotlib.pyplot as plt
import pandas as pd 
import ggplot
import numpy as np

# This function returns a list of lists that contains [type of test, starting line, ending line, middle line]
#[['static 1', 1, 48, 25], ['static 2', 49, 96, 73], ['dynamic 2', 97, 144, 121]]
def getMidPoint(NameOfFile):

	CurrentTest = ""
	CurrentIndex = 0
	MidPointList = []
	temp = 0
	for index,line in enumerate(fileinput.input(NameOfFile + ".csv",inplace=0,backup=0)):
		if index == 0:
			continue
		currentLine = re.split('(\d+)',line)
		currentLine = currentLine[0] + " " + currentLine[1]
		temp = index
		if (currentLine != CurrentTest):
			CurrentTest = currentLine
			MidPointList.append([CurrentTest,index])


			if CurrentIndex != 0:
				MidPointList[CurrentIndex -1].append(index -1)
				MidPointList[CurrentIndex -1].append((MidPointList[CurrentIndex -1][1] + index)/2) 
				# print(MidPointList[CurrentIndex -1][1])

			CurrentIndex += 1
	MidPointList[CurrentIndex-1].append(temp)
	MidPointList[CurrentIndex-1].append((MidPointList[CurrentIndex-1][1] + MidPointList[CurrentIndex-1][2] /2))
	return MidPointList

def findRepetingLine(MidPointList):
	ListOfTest = []
	EndingLine = 0
	temp = []
	for midPoint in MidPointList:
		if midPoint[0] not in ListOfTest:
			ListOfTest.append(midPoint[0])
		else:
			EndingLine = midPoint[1] -1 
			return EndingLine
		temp = midPoint
	EndingLine = temp[2]
	
	return EndingLine

def DeleteRepeat(NameOfFile,MidPointList):
	if (re.split(',',MidPointList[0][0])[0] == " "):
		return
	EndingLine = findRepetingLine(MidPointList)
	for index,line in enumerate(fileinput.input(NameOfFile + ".csv",inplace=1,backup=0)):
		if (index <= EndingLine):
			print(line.strip("\n"))


def DeleteAndInsertNameAtMid(NameOfFile,MidPointList):
	if (re.split(',',MidPointList[0][0])[0] == " "):
		return
	MidPointIndex = 0
	for index,line in enumerate(fileinput.input(NameOfFile + ".csv",inplace=1,backup=0)):
		if index == 0:
			print(line.strip('\n'))
			continue
		line = re.split(',',line)
		if index == MidPointList[MidPointIndex][3]:
			print("%s,%s" %(MidPointList[MidPointIndex][0],line[1].strip('\n')))
			MidPointIndex += 1 
		else:
			print(" ,%s" %line[1].strip('\n'))

def trimCSVFile(NameOfFile):
	var = getMidPoint(NameOfFile)
	DeleteRepeat(NameOfFile,var)

	DeleteAndInsertNameAtMid(NameOfFile,var)



def graphFile(NameOfFile,MidPointList):
	data = np.genfromtxt('ex_ifq_speed_decode_int_Table.csv', delimiter=',', skip_header=1)
	ax1 = plt.subplot(2, 1, 1)
	
	# ax1.xaxis.set_ticks(np.arange(0, 288, 1))
	# labels = [item.get_text() for item in ax1.get_xticklabels()]
	# label = [" " for x in labels]
	ax1.plot(data)
	plt.show()


def main():
	trimCSVFile("ex_ifq_speed_decode_int_Table")

	# graphFile("ex_ifq_speed_decode_int_Table",var)



if __name__ == "__main__":
    main()