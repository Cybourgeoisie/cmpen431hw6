import sys
import os
import re
import itertools

#
# See experiment_alu_mult.py in this folder for an example of usage
#

# Generate all permutations of dynamic parameters
def combineParameters(params):
	combinations = []
	for r in itertools.product(*params.values()): 
		combinations.append(dict(zip(params.keys(), r)))
	return combinations


# Validate permutations of proposed settings
def validateSettings(settings):
	
	if 'res:ialu' in settings and 'res:imult' in settings:
		if int(settings['res:ialu']) + int(settings['res:imult']) > 2 * int(settings['issue:width']):
			return False

	if 'res:fpalu' in settings and 'res:fpmult' in settings:
		if int(settings['res:fpalu']) + int(settings['res:fpmult']) > 2 * int(settings['issue:width']):
			return False

	return True


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

	return settings


# Create the configuration files for a set of dynamic and static parameters
def makeConfigs(testName, dynamicParams, staticParams):
	
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

				# Validate this combination with the current setttings
				if (validateSettings(settings) == False):
					continue

				# Construct the config name
				configName = constructConfigName(superscalar, issue_width, staticParams, params)
				
				# Save the config settings to file
				saveConfig(testName, configName, settings)



# Accept a test set, a title, and the config text
def saveConfig(testSet, title, settings):
	# Create the folder if it doesn't exist
	if (os.path.isdir("../configs/%s/%s" %(testSet,title)) != True):
		os.makedirs("../configs/%s/%s" %(testSet,title))

	# write the config
	configName = "../configs/%s/%s/config.cfg" %(testSet,title)
	with open(configName, "w") as configFile:
		configFile.writelines('-{} {}\r\n'.format(k,v) for k, v in settings.items())	

	return configName


# Construct the config name
def constructConfigName(superscalar, issue_width, staticParams, params):
	configName = superscalar + str(issue_width)
	params.update(staticParams)
	for key, value in params.items():
		if (key not in ["issue:width", "issue:inorder", "issue:wrongpath"]):
			configName += re.sub("[^a-zA-Z0-9]", "", key + str(value))
	return configName

