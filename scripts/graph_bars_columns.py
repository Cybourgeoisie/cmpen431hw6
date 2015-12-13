import sys
import numpy as np
import matplotlib.pyplot as plt

# Example usage on Mac / Linux:
# python graph_bars_columns.py ../paper/graphs/branch\ prediction/static/Branch_Prediction_static_int_Table.csv

threshold = 1000 # The geometric mean cutoff for parsed data
labels = []
data = []
parsed_data = []

with open(sys.argv[1], "rb") as input_file:
	for i, line in enumerate(input_file):
		
		# Divide the comma-separated line
		split_line = line.strip().split(',')
		
		# Get the labels and initialize the multi-dimensional lists to store data
		if i == 0:
			labels = split_line
			data = [[] for _ in range(len(split_line))]
			parsed_data = [[] for _ in range(len(split_line))]
			continue

		# Organize the data into rows
		for j, item in enumerate(split_line):
			if item:
				item = float(item)
				data[j].append(item)

				# Sift through the data for values below an ideal threshold
				if item < threshold:
					parsed_data[j].append(item)


	# Show the entire data set
	#n, bins, patches = plt.hist(data, bins=20, histtype='bar', 
	#	color=['crimson', 'burlywood', 'chartreuse'], label=labels)


	# Show only the values below threshold
	n, bins, patches = plt.hist(parsed_data, bins=20, histtype='bar', label=labels)


	# Plot the data
	plt.title(sys.argv[2])
	plt.xlabel("Geometric Mean of Execution Time (us)")
	plt.ylabel("Count")
	plt.legend()
	# plt.show()
	plt.savefig(sys.argv[2] + ".png")
