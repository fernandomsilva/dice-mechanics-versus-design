import os

def parseWorkerFiles(filepath, number_of_workers):
	files = [name for name in os.listdir(filepath + "/worker_data") if os.path.isfile(filepath + "/worker_data/" + name)]

	file_data = []
	result_vector = []
	
	total_files_parsed = 0
	for file in files:
		input_file = open(filepath + "/worker_data/" + file, 'r')

		temp = []
		for line in input_file:
			if line != "" and line != "\n":
				line_elements = line.split(';')
				temp.append((int(line_elements[1]), int(line_elements[0])))

		file_data.append(temp)
		
		input_file.close()
		
		total_files_parsed += 1
		if number_of_workers > 0 and total_files_parsed >= number_of_workers:
			break

	for i in range(0, len(file_data)):
		entry_list = file_data[i]
		
		if len(result_vector) == 0:
			for entry in entry_list:
				result_vector.append([entry[0], entry[1]])
		else:
			for j in range(0, len(entry_list)):
				result_vector[j] = [result_vector[j][0] + entry[0], result_vector[j][1] + entry[1]]

	return [(float(x[0]) / float(x[1])) for x in result_vector]