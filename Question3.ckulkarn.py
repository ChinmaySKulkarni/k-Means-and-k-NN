#!/usr/bin/python 
import sys
'''
	This program is used to implement the k-means algorithm.
'''

'''This function is used to print the correct usage for running the program.
'''
def usage():
	return "python\t<Question3.ckulkarn.py>\t<Initial_Cluster_Centers>\t<Data_Points>\t<K-value>"


def extract_intial_cluster_centers(cluster_centers_fd,k_value):
	clusters = []
	lines = cluster_centers_fd.readlines()
	if len(lines) != k_value:
		print "Difference in k_value and number of initial clusters provided!"
		sys.exit(1)
	for initial_cluster_center in lines:
		cluster = {}
		cluster['Center']= tuple(initial_cluster_center.strip().split(" "))
		cluster['Points'] = []
		clusters.append(cluster)
	return clusters
	
	
def extract_data_points(data_points_fd):
	lines = data_points_fd.readlines()
	data_points = []
	for point in lines[1:]:
		point = tuple(point.strip().split(" "))
		data_points.append(point)
	return data_points


'''This function is used to calculate the euclidean distance between the test case
	 data point and a given data point in the training set.
'''
def calculate_euclidean_distance(point,center):
	sqr_sum = 0.0
	num_coordinates = len(point)
	for index in range(0,num_coordinates):
		sqr_sum = float(sqr_sum) + float(float(point[index]) - float(center[index]))**2
	return float(sqr_sum**(0.5))


def identical(initial_clusters_points,clusters):
	num_clusters = len(initial_clusters_points)
	for cluster_number in range(0,num_clusters):
		initial_list = initial_clusters_points[cluster_number]
		current_list = clusters[cluster_number]['Points']
		length = len(initial_list)
		if length != len(current_list):
			return False
		for point in initial_list:
			if point not in current_list:
				return False
		for point in current_list:
			if point not in initial_list:
				return False
		return True


def find_cluster(point,clusters):
	for cluster in clusters:
		if point in cluster['Points']:
			return clusters.index(cluster)
	return -1


def recalculate_centers(clusters):
	dimensionality = len(clusters[0]['Points'][0])
	for cluster in clusters:
		points = cluster['Points']
		means = []
		for dim_num in range(0,dimensionality):
			mean_dim = 0.0
			for point in points:
				mean_dim = float(mean_dim) + float(point[dim_num])
			mean_dim = float(mean_dim)/float(len(points))
			means.append(mean_dim)
		cluster['Center'] = tuple(means)
	return clusters


def store_original_clusters(clusters):
	copy_clusters = []
	for orig_cluster in clusters:
		copy_clusters.append(list(orig_cluster['Points']))
	return copy_clusters
	

def run_kmeans(clusters,data_points,k_value,iteration_count):
	print "Iteration Number:\t",iteration_count
	for cluster in clusters:
		print "Cluster[" + str(clusters.index(cluster)) + "]->\t",cluster
	print "\n"
	initial_clusters_points = store_original_clusters(clusters)
	for point in data_points:
		min_dist = sys.maxint
		nearest_cluster_index = -1
		for cluster in clusters:
			dist = calculate_euclidean_distance(point,cluster['Center'])
			if dist < min_dist:
				min_dist = dist
				nearest_cluster_index = clusters.index(cluster)
		initial_cluster_of_point = find_cluster(point,clusters)
		if initial_cluster_of_point != -1:
			clusters[initial_cluster_of_point]['Points'].remove(point)
		clusters[nearest_cluster_index]['Points'].append(point)
	clusters = recalculate_centers(clusters)
	if identical(initial_clusters_points,clusters):
		return clusters
	return  run_kmeans(clusters,data_points,k_value,iteration_count + 1)


if __name__ == "__main__":
	if len(sys.argv) !=  4:
		print usage()
		sys.exit(1)
	cluster_centers_fd = open(sys.argv[1],"r")
	data_points_fd = open(sys.argv[2],"r")
	k_value = int(sys.argv[3])
	if k_value <= 0:
		print "Enter a valid positive value for k!"
		sys.exit(1)
	clusters = extract_intial_cluster_centers(cluster_centers_fd,k_value)
	data_points = extract_data_points(data_points_fd)
	final_clusters = run_kmeans(clusters,data_points,k_value,0)	
	print "Final Clusters:"
	for cluster in clusters:
		print "Cluster[" + str(clusters.index(cluster)) + "]->\t",cluster
	print "\n"
	cluster_centers_fd.close()
	data_points_fd.close()
