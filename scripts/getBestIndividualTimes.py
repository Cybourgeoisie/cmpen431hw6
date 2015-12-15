import fileinput
import os.path
import re
import subprocess
import os

import matplotlib.pyplot as plt
import pandas as pd 
import ggplot
import numpy as np

def getBestIndividualTimes():

	# Calculate best values of all tests, ever
	bestMcfTime  = 10000
	bestMilcTime = 10000
	bestMcfTest  = ""
	bestMilcTest = ""

	# get the name of all the table sets in the table folder
	tableSets = []
	for index,(subdir,dirs,files) in enumerate(os.walk("../tables/")):
		if index == 0:
			tableSets = dirs
	
	# go through all the tables and generate the geomentric means graph for them
	for table in tableSets:

		DF = pd.read_csv("../tables/%s/rawTable.csv" %(table))
		matrix = DF.as_matrix()

		if (len(matrix[0]) < 5):
			continue

		for i in range(0,len(matrix)):
			if (matrix[i][1] == 'milc' and matrix[i][4] <= bestMilcTime):
				bestMilcTime = matrix[i][4]
				bestMilcTest = matrix[i][0]
			elif (matrix[i][1] == 'mcf' and matrix[i][4] <= bestMcfTime):
				bestMcfTime = matrix[i][4]
				bestMcfTest = matrix[i][0]

	print bestMilcTime
	print bestMilcTest
	print bestMcfTime
	print bestMcfTest


getBestIndividualTimes()
