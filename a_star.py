import sys
import yaml

# List where the path will be stored
path = []

# Class node
class Node:
	def __init__(self, name, heuristic):
		self.name = name
		self.neighbors = []
		self.g_score = {}
		self.heuristic = heuristic

	def set_neighbors(self, graph, neighbors):
		for neighbor in neighbors.get(self.name):
			self.neighbors.append(graph.get(neighbor))

	def get_neighbors(self):
		return self.neighbors

	def set_costs(self, cost):
		for neighbor in self.neighbors:
			self.g_score.update({neighbor : cost})

	def get_costs(self):
		for neighbor in self.neighbors:
			print(self.g_score.get(neighbor))

	def get_gscore(self, neighbor):
		return self.g_score.get(neighbor)

# Backtrack to get the path if A* succeeds
def get_path(previous_node_in_path, start, goal):
	global path
	
	# while there are objects in the dicrionary
	while previous_node_in_path:
		# append the goal node and go to the previous one
		if goal not in path:
			path.insert(0, goal)
			next_node = previous_node_in_path.get(goal)
			del previous_node_in_path[goal]
		# append the current node and go to the previous one
		else:
			path.insert(0, next_node)
			try:
				next_node_key = previous_node_in_path.get(next_node)
				del previous_node_in_path[next_node]
				next_node = next_node_key
			except:
				previous_node_in_path = {}


# A* implementation
def a_star(nodes, start, goal):

	# dictionary to keep track of f_scores for each node
	open_set = {}
	open_set.update({0 : start})

	# dictionary to keep the previous node of each node in the final path
	# used to get the path at the end of the algorithm
	previous_node_in_path = {}
	
	# g_score for each node
	g_score = {node : float("inf") for node in nodes}
	g_score[start] = 0

	# f_score for each node
	f_score = {node : float("inf") for node in nodes}
	f_score[start] = start.heuristic

	# set of nodes to be processed
	open_set_hash = {start}

	# while there are nodes to be processed
	while open_set:
		# get the node with the lowest f_score and remove it
		current = open_set[min(list(open_set.keys()))]
		del open_set[min(list(open_set.keys()))]
		open_set_hash.remove(current)

		# if the current node is the goal node, end the algo and get the path
		if current == goal:
			get_path(previous_node_in_path, start.name, goal.name)
			return True

		# for each neighbor
		for neighbor in current.neighbors:

			# compute the new g_score
			temp_g_score = g_score[current] + current.get_gscore(neighbor)

			# if new g_score is less than the last one, update the g_score, f_score
			# and add the node to the open_set if it does not exist or update its f_score
			# in order to be processed later
			if temp_g_score < g_score[neighbor]:
				previous_node_in_path[neighbor.name] = current.name
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + neighbor.heuristic
				if neighbor not in open_set_hash:
					open_set.update({f_score.get(neighbor) : neighbor})
					open_set_hash.add(neighbor)

	return False


# Parse the yaml file, create the node objects and call A*
def main():
	global path
	# open yaml file
	graph_file = yaml.load(open(sys.argv[1], 'r'), Loader=yaml.FullLoader)
	
	graph = []
	graph_dict = {}

	# Create nodes
	for node in graph_file['nodes']:
		if node == graph_file['start']:
			start_node = Node(node, graph_file['heuristics'][node]) 
			graph.append(start_node)
		elif node == graph_file['goal']:
			goal_node = Node(node, graph_file['heuristics'][node])
			graph.append(goal_node)
		else:
			other_node = Node(node, graph_file['heuristics'][node])
			graph.append(other_node)
		
		graph_dict.update({node : graph[-1]})

	# Set neighbors and edge costs
	for node in graph:
		node.set_neighbors(graph_dict, graph_file['neighbors'])
		node.set_costs(graph_file['edge_costs'])

	# call A* and print the path if it exists
	print (path) if (a_star(graph, start_node, goal_node)) else print("Path not found")



if __name__ == "__main__":
	main()