import sys
import os
import re
import itertools

#
# See experiment_alu_mult.py in this folder for an example of usage
#

debug = False
forceOptimal = False


# Validate permutations of proposed settings
def validateSettings(settings):

	if not validateL1Cache(settings):
		if debug:
			print("Failed L1 cache validation.")
		return False

	if not validateL2Cache(settings):
		if debug:
			print("Failed L2 cache validation.")
		return False

	if not validateTlb(settings):
		if debug:
			print("Failed TLB validation.")
		return False

	if not validateBped(settings):
		if debug:
			print("Failed BPred validation.")
		return False

	if not validateFunctionalUnits(settings):
		if debug:
			print("Failed functional unit validation.")
		return False

	if not validateMemory(settings):
		if debug:
			print("Failed memory validation.")
		return False
	
	if not validateMisc(settings):
		if debug:
			print ("Failed misc validation.")
		return False


	return True

# Validate cache:il1, cache:dl1, il1lat, dl1lat
def validateL1Cache(settings):

	il1 = re.split(':',settings['cache:il1'])
	dl1 = re.split(':',settings['cache:dl1'])

	# Constraint: il1 block size must match the ifq size and dl1 block size
	if ( int(il1[2]) != int(settings['fetch:ifqsize']) * 8 ) or ( int(il1[2]) != int(dl1[2]) ):
		return False

	# Constraint: 
			# * il1 & dl1 latencies are defined by the il1 sizes:
		 #  * All of the below also hold for dl1
		 #  * Direct mapped:
		 #    * il1 = 8 KB (baseline, minimum size) means il1lat = 1
		 #    * il1 = 16 KB means il1lat = 2
		 #    * il1 = 32 KB means il1lat = 3
		 #    * il1 = 64 KB (maximum size) means il1lat = 4
		if int(il1[3]) == 1:
			if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 8192 ) and ( int(settings['cache:il1lat'] != 1) ):
				return False

			if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 16384 ) and ( int(settings['cache:il1lat'] != 2) ):
				return False
			
			if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 32768 ) and ( int(settings['cache:il1lat'] != 3) ):
				return False
			
			if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 65536 ) and ( int(settings['cache:il1lat'] != 4) ):
				return False

		if int(dl1[3]) == 1:
			if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 8192 ) and ( int(settings['cache:dl1lat'] != 1) ):
				return False

			if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 16384 ) and ( int(settings['cache:dl1lat'] != 2) ):
				return False
			
			if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 32768 ) and ( int(settings['cache:dl1lat'] != 3) ):
				return False
			
			if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 65536 ) and ( int(settings['cache:dl1lat'] != 4) ):
				return False

		 #  * 2-way set associative:
		 #    * il1 = 8 KB (baseline, minimum size) means il1lat = 2
		 #    * il1 = 16 KB means il1lat = 3
		 #    * il1 = 32 KB means il1lat = 4
		 #    * il1 = 64 KB (maximum size) means il1lat = 5
		if int(il1[3]) == 2:
			if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 8192 ) and ( int(settings['cache:il1lat'] != 2) ):
				return False

			if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 16384 ) and ( int(settings['cache:il1lat'] != 3) ):
				return False
			
			if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 32768 ) and ( int(settings['cache:il1lat'] != 4) ):
				return False
			
			if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 65536 ) and ( int(settings['cache:il1lat'] != 5) ):
				return False

		if int(dl1[3]) == 2:
			if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 8192 ) and ( int(settings['cache:dl1lat'] != 2) ):
				return False

			if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 16384 ) and ( int(settings['cache:dl1lat'] != 3) ):
				return False
			
			if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 32768 ) and ( int(settings['cache:dl1lat'] != 4) ):
				return False
			
			if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 65536 ) and ( int(settings['cache:dl1lat'] != 5) ):
				return False
		 #  * 4-way set associative:
		 #    * il1 = 8 KB (baseline, minimum size) means il1lat = 3
		 #    * il1 = 16 KB means il1lat = 4
		 #    * il1 = 32 KB means il1lat = 5
		 #    * il1 = 64 KB (maximum size) means il1lat = 6
		if int(il1[3]) == 4:
			if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 8192 ) and ( int(settings['cache:il1lat'] != 3) ):
				return False

			if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 16384 ) and ( int(settings['cache:il1lat'] != 4) ):
				return False
			
			if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 32768 ) and ( int(settings['cache:il1lat'] != 5) ):
				return False
			
			if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 65536 ) and ( int(settings['cache:il1lat'] != 6) ):
				return 

		if int(dl1[3]) == 4:
			if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 8192 ) and ( int(settings['cache:dl1lat'] != 3) ):
				return False

			if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 16384 ) and ( int(settings['cache:dl1lat'] != 4) ):
				return False
			
			if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 32768 ) and ( int(settings['cache:dl1lat'] != 5) ):
				return False
			
			if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 65536 ) and ( int(settings['cache:dl1lat'] != 6) ):
				return False

	return True


# Validate cache:dl2, cache:dl2lat, cache:il2lat
def validateL2Cache(settings):

	ul2 = re.split(':',settings['cache:dl2'])
	# Constraint: 
	 # * ul2 latencies are defined by the ul2 sizes:
	 #  * Direct mapped:
	 #    * ul2 = 64KB (baseline, minimum size) means ul2lat = 4
	 #    * ul2 = 128 KB means ul2lat = 5
	 #    * ul2 = 256 KB means ul2lat = 6
	 #    * ul2 = 512 KB means ul2 lat = 7
	 #    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 8
	if int(ul2[3]) == 1:
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 65536 ) and ( int(settings['cache:dl2lat'] != 4 or int(settings['cache:il2lat'] != 4) ) ):
				return False

			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 131072 ) and ( int(settings['cache:dl2lat'] != 5 or int(settings['cache:il2lat'] != 5) ) ):
				return False
			
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 262144 ) and ( int(settings['cache:dl2lat'] != 6 or int(settings['cache:il2lat'] != 6) ) ):
				return False
			
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 524288 ) and ( int(settings['cache:dl2lat'] != 7 or int(settings['cache:il2lat'] != 7) ) ):
				return False

			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 1048576 ) and ( int(settings['cache:dl2lat'] != 8 or int(settings['cache:il2lat'] != 8) ) ):
				return False
	 #  * 2-way set associative:
	 #    * ul2 = 64KB (baseline, minimum size) means ul2lat = 5
	 #    * ul2 = 128 KB means ul2lat = 6
	 #    * ul2 = 256 KB means ul2lat = 7
	 #    * ul2 = 512 KB means ul2 lat = 8
	 #    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 9
	if int(ul2[3]) == 2:
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 65536 ) and ( int(settings['cache:dl2lat'] != 5 or int(settings['cache:il2lat'] != 5) ) ):
				return False

			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 131072 ) and ( int(settings['cache:dl2lat'] != 6 or int(settings['cache:il2lat'] != 6) ) ):
				return False
			
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 262144 ) and ( int(settings['cache:dl2lat'] != 7 or int(settings['cache:il2lat'] != 7) ) ):
				return False
			
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 524288 ) and ( int(settings['cache:dl2lat'] != 8 or int(settings['cache:il2lat'] != 8) ) ):
				return False

			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 1048576 ) and ( int(settings['cache:dl2lat'] != 9 or int(settings['cache:il2lat'] != 9) ) ):
				return False
	 #  * 4-way set associative:
	 #    * ul2 = 64KB (baseline, minimum size) means ul2lat = 6
	 #    * ul2 = 128 KB means ul2lat = 7
	 #    * ul2 = 256 KB means ul2lat = 8
	 #    * ul2 = 512 KB means ul2 lat = 9
	 #    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 10
	if int(ul2[3]) == 4:
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 65536 ) and ( int(settings['cache:dl2lat'] != 6 or int(settings['cache:il2lat'] != 6) ) ):
				return False

			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 131072 ) and ( int(settings['cache:dl2lat'] != 7 or int(settings['cache:il2lat'] != 7) ) ):
				return False
			
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 262144 ) and ( int(settings['cache:dl2lat'] != 8 or int(settings['cache:il2lat'] != 8) ) ):
				return False
			
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 524288 ) and ( int(settings['cache:dl2lat'] != 9 or int(settings['cache:il2lat'] != 9) ) ):
				return False

			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 1048576 ) and ( int(settings['cache:dl2lat'] != 10 or int(settings['cache:il2lat'] != 10) ) ):
				return False
	 #  * 8-way set associative:
	 #    * ul2 = 64KB (baseline, minimum size) means ul2lat = 7
	 #    * ul2 = 128 KB means ul2lat = 8
	 #    * ul2 = 256 KB means ul2lat = 9
	 #    * ul2 = 512 KB means ul2 lat = 10
	 #    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 11
	if int(ul2[3]) == 8:
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 65536 ) and ( int(settings['cache:dl2lat'] != 7 or int(settings['cache:il2lat'] != 7) ) ):
				return False

			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 131072 ) and ( int(settings['cache:dl2lat'] != 8 or int(settings['cache:il2lat'] != 8) ) ):
				return False
			
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 262144 ) and ( int(settings['cache:dl2lat'] != 9 or int(settings['cache:il2lat'] != 9) ) ):
				return False
			
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 524288 ) and ( int(settings['cache:dl2lat'] != 10 or int(settings['cache:il2lat'] != 10) ) ):
				return False

			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 1048576 ) and ( int(settings['cache:dl2lat'] != 11 or int(settings['cache:il2lat'] != 11) ) ):
				return False
	 #  * 16-way set associative:
	 #    * ul2 = 64KB (baseline, minimum size) means ul2lat = 8
	 #    * ul2 = 128 KB means ul2lat = 9
	 #    * ul2 = 256 KB means ul2lat = 10
	 #    * ul2 = 512 KB means ul2 lat = 11
	 #    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 12
	if int(ul2[3]) == 16:
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 65536 ) and ( int(settings['cache:dl2lat'] != 8 or int(settings['cache:il2lat'] != 8) ) ):
				return False

			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 131072 ) and ( int(settings['cache:dl2lat'] != 9 or int(settings['cache:il2lat'] != 9) ) ):
				return False
			
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 262144 ) and ( int(settings['cache:dl2lat'] != 10 or int(settings['cache:il2lat'] != 10) ) ):
				return False
			
			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 524288 ) and ( int(settings['cache:dl2lat'] != 11 or int(settings['cache:il2lat'] != 11) ) ):
				return False

			if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 1048576 ) and ( int(settings['cache:dl2lat'] != 12 or int(settings['cache:il2lat'] != 12) ) ):
				return False


	return True

# Validate tlb:itlb abd tlb:dtlb
def validateTlb(settings):

	# Constraint: itlb entries: 1,2,4,8,16,32,64,128,256
	itlb = re.split(':',settings['tlb:itlb'])
	if not (int(itlb[1]) * int(itlb[3])) in [1,2,4,8,16,32,64,128,256]:
		return False

	# Constraint: dtlb entries: 1,2,4,8,16,32,64,128,256,512
	dtlb = re.split(':',settings['tlb:dtlb'])
	if not (int(dtlb[1]) * int(dtlb[3])) in [1,2,4,8,16,32,64,128,256,512]:
		return False

	return True

# Validate fetch:speed, fetch:ifqsize, decode:width, ruu:size and lsq:size
def validateMisc(settings):

	# Constraint: fetch:speed ratio max is 4
	if int(settings['fetch:speed']) > 4:
		return False

	# Constraint: ifqsize can be set to a maximum of 16 words (128B)
	if int(settings['fetch:ifqsize']) > 16:
		return False

	# Constraint: decode:width <= fetch:ifqsize; decode:width = 1, 2, 4, 8
	if (int(settings['decode:width']) > int(settings['fetch:ifqsize'])) or (not int(settings['decode:width']) in [1,2,4,8,16]):
		return False

	# Constraint: ruu:size - no more than 8 times the issue width, max 64
	if (int(settings['ruu:size']) > int(settings['issue:width']) * 8):
		return False

	# Constraint: lsq:size - no more than 4 times the issue width, max 32
	if (int(settings['lsq:size']) > int(settings['issue:width']) * 4):
		return False

	return True


# Validate bpred, bpred:ras and bpred:btb
def validateBped(settings):

	# Constraint: bpred can be any EXCEPT perfect
	if settings['bpred'] == "perfect":
		return False

	# Constraint: bpred:ras between 0 and 16, inclusive
	if (int(settings['bpred:ras']) not in range(0,17)):
		return False 

	# Constraint: bpred:btb max of 1024 sets, 1-, 2-, 4-way
	# 	Comment: Ben we are defaulting to 4 way here. Do we want to change the associativity in the future?
	if ( int(settings['bpred:btb'].split(" ")[0]) > 1024 ) or not( int(settings['bpred:btb'].split(" ")[1]) in [1,2,4] ):
		return False

	return True


# Validate res:memport and mem:width
def validateMemory(settings):

	# Constraint: res:memport = 1, 2
	if not ( int(settings['res:memport']) == 1 or int(settings['res:memport']) == 2 ):
		return False;

	# Constraint: mem:width = 8 , 16
	if not ( int(settings['mem:width']) == 8 or int(settings['mem:width']) == 16 ):
		return False;

	return True


# Validate res:imult, res:ialu, res:falu, res:fpmult
def validateFunctionalUnits(settings):

	# Constraint: number of integer ALU's / mult/div's must be <= MAX_INSTS_PER_CLASS
	if int(settings['res:ialu']) > 8 or int(settings['res:imult']) > 8:
		return False;

	# Constraint: number of FP ALU's / mult/div's must be <= MAX_INSTS_PER_CLASS
	if int(settings['res:fpalu']) > 8 or int(settings['res:fpmult']) > 8:
		return False;

	# Project constraint: imult + ialu <= 2 * issue:width
	if int(settings['res:ialu']) + int(settings['res:imult']) > 2 * int(settings['issue:width']):
		return False

	# Project constraint: fpmult + fpalu <= 2 * issue:width
	if int(settings['res:fpalu']) + int(settings['res:fpmult']) > 2 * int(settings['issue:width']):
		return False

	return True


# Generate all permutations of dynamic parameters
def combineParameters(params):
	combinations = []
	for r in itertools.product(*params.values()): 
		combinations.append(dict(zip(params.keys(), r)))
	return combinations

# Parse a config file, pull all of the configs out into a settings dictionary
def getSettingsFromFile(filename):
	# Get the config file
	f = open(filename)

	# Construct settings from the file
	settings = {}
	for line in f:
		if line.startswith('-') == True:
			splitLine = re.split("\s+", line)
			settings[re.sub('-','',splitLine[0])] = splitLine[1]

			# The above works for everything except mem:lat,bpred:2lev, and bpred:btb, which has two parameters separated by a space
			if splitLine[0] == "-mem:lat":
				settings[re.sub('-','',splitLine[0])] += " " + splitLine[2]
			if splitLine[0] == "-bpred:2lev":
				settings[re.sub('-','',splitLine[0])] += " " + splitLine[2] + " " + splitLine[3] + " " + splitLine[4]
			if splitLine[0] == "-bpred:btb":
				settings[re.sub('-','',splitLine[0])] += " " + splitLine[2]

	return settings


# Create the configuration files for a set of dynamic and static parameters
def makeConfigs(testName, dynamicParams, staticParams, overrideIssueWidths = {}, useOptimal = False):
	
	# Make the baseline config
	settings = getSettingsFromFile('../configs/baseline.cfg')

	# Parse the dynamic parameters, return the final list of combinations
	combinations = combineParameters(dynamicParams)

	# For static and dynamic..
	for superscalar in ("static", "dynamic"):

		# Set the configs that make the simulation either static or dynamic
		settings['issue:inorder']   = 'true'  if (superscalar == "static") else 'false'
		settings['issue:wrongpath'] = 'false' if (superscalar == "static") else 'true'

		# Change all of the static parameters
		settings.update(staticParams)

		# Run the tests for all issue widths
		if overrideIssueWidths is not {} and superscalar in overrideIssueWidths:
			issue_widths = overrideIssueWidths[superscalar]
		else:
			if (superscalar == "static"):
				issue_widths = [1,2,4]
			elif (superscalar == "dynamic"):
				issue_widths = [2,4,8]

		# For each available issue width...
		for issue_width in issue_widths:
			
			# Set the current issue width
			settings['issue:width'] = issue_width

			# Run test for each set of combinations
			for params in combinations:

				# Include the current dynamic settings
				settings.update(params)

				# Set optimal values
				if forceOptimal or useOptimal:
					settings = setOptimalVariables(superscalar, issue_width, settings)
				
				# Set the absolute dependent variables
				settings = setDependentVariables(settings)

				# Validate this combination with the current setttings
				if (validateSettings(settings) == False):
					continue

				# Construct the config name
				configName = constructConfigName(superscalar, issue_width, staticParams, params)
				
				# Save the config settings to file
				saveConfig(testName, configName, settings)


def setOptimalVariables(superscalar, issue_width, settings):

	# Can't set here, but good to write down:
	# ifqsize - should not be 4, 8 or 16

	# Max out the RUU and LSQ
	if superscalar == 'dynamic' and issue_width == 2:
		settings['ruu:size'] = 16
		settings['lsq:size'] = 8
	elif superscalar == 'dynamic' and issue_width == 4:
		settings['ruu:size'] = 32
		settings['lsq:size'] = 16
	elif superscalar == 'dynamic' and issue_width == 8:
		settings['ruu:size'] = 64
		settings['lsq:size'] = 32

	# Max out the mem:width
	settings['mem:width'] = 16

	# TEST: Make the dl1 and il1 caches equal
	#if 'cache:il1' in settings:
	#	dl1cache = list(settings['cache:il1'])
	#	dl1cache[0] = 'd' # Change from i to d
	#	settings['cache:dl1'] = "".join(dl1cache)

	return settings


# For any dependent variables, set these automatically
def setDependentVariables(settings):
	# Cache latencies
	settings = setCacheDependentVariables(settings)

	return settings

def setCacheDependentVariables(settings):
	# Set cache values
	il1 = re.split(':',settings['cache:il1'])
	dl1 = re.split(':',settings['cache:dl1'])

	if int(il1[3]) == 1:
		if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 8192 ):
			settings['cache:il1lat'] = 1

		if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 16384 ):
			settings['cache:il1lat'] = 2
		
		if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 32768 ):
			settings['cache:il1lat'] = 3
		
		if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 65536 ):
			settings['cache:il1lat'] = 4

	if int(dl1[3]) == 1:
		if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 8192 ):
			settings['cache:dl1lat'] = 1

		if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 16384 ):
			settings['cache:dl1lat'] = 2
		
		if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 32768 ):
			settings['cache:dl1lat'] = 3
		
		if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 65536 ):
			settings['cache:dl1lat'] = 4


	 #  * 2-way set associative:
	 #    * il1 = 8 KB (baseline, minimum size) means il1lat = 2
	 #    * il1 = 16 KB means il1lat = 3
	 #    * il1 = 32 KB means il1lat = 4
	 #    * il1 = 64 KB (maximum size) means il1lat = 5
	if int(il1[3]) == 2:
		if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 8192 ):
			settings['cache:il1lat'] = 2

		if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 16384 ):
			settings['cache:il1lat'] = 3
		
		if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 32768 ):
			settings['cache:il1lat'] = 4
		
		if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 65536 ):
			settings['cache:il1lat'] = 5

	if int(dl1[3]) == 2:
		if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 8192 ):
			settings['cache:dl1lat'] = 2

		if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 16384 ):
			settings['cache:dl1lat'] = 3
		
		if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 32768 ):
			settings['cache:dl1lat'] = 4
		
		if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 65536 ):
			settings['cache:dl1lat'] = 5

	 #  * 4-way set associative:
	 #    * il1 = 8 KB (baseline, minimum size) means il1lat = 3
	 #    * il1 = 16 KB means il1lat = 4
	 #    * il1 = 32 KB means il1lat = 5
	 #    * il1 = 64 KB (maximum size) means il1lat = 6
	if int(il1[3]) == 4:
		if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 8192 ):
			settings['cache:il1lat'] = 3

		if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 16384 ):
			settings['cache:il1lat'] = 4
		
		if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 32768 ):
			settings['cache:il1lat'] = 5
		
		if ( (int(il1[1]) * int(il1[2]) * int(il1[3])) == 65536 ):
			settings['cache:il1lat'] = 6

	if int(dl1[3]) == 4:
		if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 8192 ):
			settings['cache:dl1lat'] = 3

		if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 16384 ):
			settings['cache:dl1lat'] = 4
		
		if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 32768 ):
			settings['cache:dl1lat'] = 5
		
		if ( (int(dl1[1]) * int(dl1[2]) * int(dl1[3])) == 65536 ):
			settings['cache:dl1lat'] = 6


	ul2 = re.split(':',settings['cache:dl2'])

	# Constraint: 
	 # * ul2 latencies are defined by the ul2 sizes:
	 #  * Direct mapped:
	 #    * ul2 = 64KB (baseline, minimum size) means ul2lat = 4
	 #    * ul2 = 128 KB means ul2lat = 5
	 #    * ul2 = 256 KB means ul2lat = 6
	 #    * ul2 = 512 KB means ul2 lat = 7
	 #    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 8
	if int(ul2[3]) == 1:
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 65536 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 4

		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 131072 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 5
		
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 262144 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 6
		
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 524288 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 7

		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 1048576 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 8

	 #  * 2-way set associative:
	 #    * ul2 = 64KB (baseline, minimum size) means ul2lat = 5
	 #    * ul2 = 128 KB means ul2lat = 6
	 #    * ul2 = 256 KB means ul2lat = 7
	 #    * ul2 = 512 KB means ul2 lat = 8
	 #    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 9
	if int(ul2[3]) == 2:
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 65536 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 5

		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 131072 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 6
		
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 262144 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 7
		
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 524288 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 8

		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 1048576 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 9

	 #  * 4-way set associative:
	 #    * ul2 = 64KB (baseline, minimum size) means ul2lat = 6
	 #    * ul2 = 128 KB means ul2lat = 7
	 #    * ul2 = 256 KB means ul2lat = 8
	 #    * ul2 = 512 KB means ul2 lat = 9
	 #    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 10
	if int(ul2[3]) == 4:
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 65536 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 6

		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 131072 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 7
		
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 262144 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 8
		
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 524288 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 9

		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 1048576 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 10

	 #  * 8-way set associative:
	 #    * ul2 = 64KB (baseline, minimum size) means ul2lat = 7
	 #    * ul2 = 128 KB means ul2lat = 8
	 #    * ul2 = 256 KB means ul2lat = 9
	 #    * ul2 = 512 KB means ul2 lat = 10
	 #    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 11
	if int(ul2[3]) == 8:
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 65536 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 7

		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 131072 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 8
		
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 262144 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 9
		
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 524288 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 10

		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 1048576 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 11

	 #  * 16-way set associative:
	 #    * ul2 = 64KB (baseline, minimum size) means ul2lat = 8
	 #    * ul2 = 128 KB means ul2lat = 9
	 #    * ul2 = 256 KB means ul2lat = 10
	 #    * ul2 = 512 KB means ul2 lat = 11
	 #    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 12
	if int(ul2[3]) == 16:
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 65536 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 8

		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 131072 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 9
		
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 262144 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 10
		
		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 524288 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 11

		if ( (int(ul2[1]) * int(ul2[2]) * int(ul2[3])) == 1048576 ):
			settings['cache:dl2lat'] = settings['cache:il2lat'] = 12

	return settings


# Accept a test set, a title, and the config text
def saveConfig(testSet, title, settings):
	# Create the folder if it doesn't exist
	if (os.path.isdir("../configs/%s/%s" %(testSet,title)) != True):
		os.makedirs("../configs/%s/%s" %(testSet,title))

	# write the config
	configName = "../configs/%s/%s/config.cfg" %(testSet,title)
	with open(configName, "w") as configFile:
		configFile.writelines('-{0} {1}\n'.format(k,v) for k, v in settings.items())	

	return configName


# Construct the config name
def constructConfigName(superscalar, issue_width, staticParams, params):
	configName = superscalar + str(issue_width)
	params.update(staticParams)
	for key, value in params.items():
		if (key not in ["issue:width", "issue:inorder", "issue:wrongpath"]):
			configName += re.sub("[^a-zA-Z0-9]", "", key + str(value))
	return configName

