#!/usr/bin/python 
'''
	 This program is used to implement the k-nearest neighbor algorithm for classification.
	 The training data file, testing data file and the value of k must be provided as a command line argument.
	 The program prints the predicted labels for the testing set and also prints the training error observed.
'''
import sys
import random


'''This function is used to print the correct usage for running the program.
'''
def usage():
	return "python\t<Question2.1.ckulkarn.py>\t<training_data>\t<testing_data>\t<K-value>"


'''This function is used to parse the training and testing files so that 
	 the examples are stored in the form of a list of dictionaries where the 
	 keys of the dictionaries are the attribute values for an example.
'''
def parse(fd):
	data_set = []
	lines = fd.readlines()
	keys = lines[0].strip().split(" ")															#Store the keys i.e. the attribute names and the label.
	for line in lines[1:]:
		example = {}
		line = line.strip().split()
		index = 0
		for key_val in line:
			example[keys[index]] = float(key_val)												#Store the attribute values for the training and testing data points.
			index += 1
		data_set.append(example)
	return data_set


'''This function is used to calculate the euclidean distance between the test case
	 data point and a given data point in the training set.
'''
def calculate_euclidean_distance(test_case,example,keys):
	sqr_sum = 0.0
	for key in keys:
		sqr_sum = float(sqr_sum) + float(float(test_case[key]) - float(example[key]))**2
	return float(sqr_sum**(0.5))


'''This function is used for implementing the knn algorithm.
'''
def find_knn(training_data,testing_data,k_val):
	labels = ["-1","+1"]																						#Possible labels.
	keys = training_data[0].keys()
	keys.remove("y")	
	predicted_labels = []
	for test_case in testing_data:																	#Iterate over all the test data.
		nearest_neighbors = {}
		num_examples = len(training_data)
		for index in range(0,num_examples):
			nearest_neighbors[index] = calculate_euclidean_distance(test_case,training_data[index],keys)
		key_val_pair = nearest_neighbors.items()
		sort_by_distance = sorted(key_val_pair,key=lambda  x: x[1])
		k_nearest = sort_by_distance[:k_val]													#After sorting the euclidean distance, pick out the 'k' smallest values
		label = 0
		for item in k_nearest:
			label += training_data[item[0]]['y']												#Find out the label of the k-nearest neighbors.
		if label > 0:																									#Assigne the majority value label to the test data point.
			predicted_labels.append("+1")
		elif label < 0:
			predicted_labels.append("-1")
		else:
			random_index = random.randint(0,1)											
			predicted_labels.append(labels[random_index])								#Assign a random label in case there is a tie.
	return predicted_labels


'''This function is used to find the training error by comparing the
	 predicted labels to the actual given labels.
'''
def find_error(predicted_labels,testing_set):
	num_cases = len(testing_set)
	error_count = 0
	for index in range(0,num_cases):
		if testing_set[index]['y'] != float(predicted_labels[index]):
			error_count += 1
	return float(error_count)/float(num_cases)


if __name__ == "__main__":
	if len(sys.argv) != 4:
		print usage()
		sys.exit(1)
	fd_train = open(sys.argv[1],"r")
	fd_test = open(sys.argv[2],"r")
	k_val = int(sys.argv[3])
	if k_val <= 0:
		print "Enter a valid positive value for k!"
		sys.exit(1)
	training_set = parse(fd_train)
	testing_set = parse(fd_test)
	predicted_labels = find_knn(training_set,testing_set,k_val)
	print "predicted_labels:\t",predicted_labels
	error = find_error(predicted_labels,testing_set)	
	print "Testing Error\t\t",error
	fd_train.close()
	fd_test.close()
