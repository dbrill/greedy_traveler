#!/usr/bin/env python
import matplotlib.pyplot as plt
import networkx as nx
import time
import random
import doctest
import copy
import sys

def node_distance(node_1, node_2):
	"""
	returns the Euclidean distance between two points.

	input: two tuples (node_1, node_2)
	output: integer representing Euclidean distance between the two points

	>>> node_distance((10, 31), (5, 15))
	16.76305461424021
	"""
	distance = ((node_1[0] - node_2[0])**2 + (node_1[1] - node_2[1])**2)**.5
	return distance

def total_distance(nodes):
	"""
	returns the total distance of a path of nodes.

	input: list of tuples
	output: integer representing total distance traveled along path
	"""
	distance = 0
	for i in range(len(points)-1):
		distance = distance + node_distance(nodes[i], nodes[i+1])
	return distance

def BF_travelling_salesman(cities):
    """
    Bruteforce method of visiting all cities.
    Time complexity: O(n!)

	input: list of tuples
    output: shortest path to visit each city
    """
    tempperms = permutations(cities)
    perms = list(tempperms)
    minL = 999999
    minInd = 0
    for i in range(len(perms)):
        if(total_distance(perms[i]) < minL):
            minL = total_distance(perms[i])
            minInd = i
    result = list(perms[minInd])
    result.reverse()
    return perms[minInd]

def greedy_travelling_salesman(cities, start):
	"""
	Greedy solution to travelling salesman where we visit the nearest non-visited city first
	Complexity = O(n^2)

	input: Dictionary of cities as tuples and starting city as a tuple
	output: index of nodes representing optimal path to visit each city once

	>>> greedy_travelling_salesman({0: [3,1], 1: [13,0], 2: [9,7], 3: [0, 5]})
	[0, 3, 2, 1]
	"""
	start = cities.keys()[0]
	unvisited = copy.deepcopy(cities)
	greedy_path = [start]
	del unvisited[start]

	while len(unvisited) != 0:
		closestCity = (-1, -1)
		for i in unvisited:
			#if min not yet set
			if closestCity[0] == -1:
				closestCity = (i, node_distance(cities[greedy_path[-1]], unvisited[i]))
			else:
				dist = node_distance(cities[greedy_path[-1]], unvisited[i])
				if closestCity[1] > dist:
					closestCity = (i, dist)
		greedy_path.append(closestCity[0])
		del unvisited[closestCity[0]]
	return greedy_path

def main(num_nodes, edges, weights):
	random.seed()
	G=nx.path_graph(0)
	pos = {}
	#gen points
	for i in range(num_nodes):
		pos[i] = (random.randint(0, 5 * num_nodes), random.randint(0, 5 * num_nodes))
	#gen node for each element in pos
	G.add_nodes_from(pos.keys())
	size = len(G.nodes(False))
	fig, ax = plt.subplots(num=None, figsize=(13, 8), facecolor='w', edgecolor='k')
	if edges:
		#adds edges to nodes, ***possibly remove this***
		for i in range(size):
			nextN = i+1
			if(i == size-1):
				G.add_edge(0, i, weight=int(node_distance(pos[0], pos[i])))
				nextN = 0
			G.add_edge(i, nextN, weight=int(node_distance(pos[i], pos[nextN])))

			#get edge weights
		labels = nx.get_edge_attributes(G,'weight')
		if weights:
			nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
	#initialize random node positions
	for n, p in pos.iteritems():
		G.node[n] = p
	#get travel path
	path = greedy_travelling_salesman(G.node,0)
	path.append(path[0])
	path_edges=zip(path, path[1:])
	plt.title("Nearest Neighbor Traveling Salesman Implementation!")
	nx.draw(G, pos, with_labels=True, k=.9)
	plt.ion()
	#walk travel path
	for i in range(len(path)-1):
		nx.draw_networkx_nodes(G,pos,nodelist=[path[i]],node_color='g')
		nx.draw_networkx_edges(G,pos,edgelist=[path_edges[i]],edge_color='g',width=4)
		plt.pause(1.0 / float(num_nodes))
	nx.draw_networkx_nodes(G,pos,nodelist=[path[len(path)-1]],node_color='g')
	plt.show()
	#make figure persisten after finishing
	while True:
		plt.pause(.05)

edges = False
weights = False
num_nodes = input("please input a number of nodes: ")
while(type(num_nodes) != int):
	num_nodes = input("Please input an integer value for the number of nodes: ")
if(len(sys.argv) >= 2):
	edges = True
if(len(sys.argv) >= 3):
	edges = True
	weights = True

main(num_nodes, edges, weights)
