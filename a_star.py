import sys
import yaml

# List where the path will be stored
path = []

# Helping dictionary
node_dict = {}

# Class node
class Node:
	def __init__(self, name, neighbors, heuristic, cost):
		self.name = name
		self.heuristic = heuristic
		self.neighbors = neighbors
		self.g_score = {}
		for neighbor in self.neighbors:
			self.g_score[neighbor] = cost

	def get_gscore(self, neighbor):
		return self.g_score[neighbor]

# Backtrack to get the path if A* succeeds
def get_path(previous_node_in_path, start, goal):
	global path
	
	# while there are objects in the dicrionary
	while previous_node_in_path:
		# append the goal node and go to the previous one
		if goal not in path:
			path.append(goal)
			next_node = previous_node_in_path[goal]
			del previous_node_in_path[goal]
		# append the current node and go to the previous one
		else:
			path.append(next_node)
			try:
				next_node_key = previous_node_in_path[next_node]
				del previous_node_in_path[next_node]
				next_node = next_node_key
			except:
				previous_node_in_path = {}
	# reverse the path so its form is start -> ... -> goal
	path = path[::-1]


# A* implementation
def a_star(nodes, start, goal):
	global node_dict

	# dictionary to keep track of f_scores for each node
	open_set = {}
	open_set.update({0 : start})

	# dictionary to keep the previous node of each node in the final path
	# used to get the path at the end of the algorithm
	previous_node_in_path = {}
	
	# g_score for each node
	g_score = {node.name : float("inf") for node in nodes}
	g_score[start.name] = 0

	# f_score for each node
	f_score = {node.name : float("inf") for node in nodes}
	f_score[start.name] = start.heuristic

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
			neighbor_node = node_dict[neighbor]

			# compute the new g_score
			temp_g_score = g_score[current.name] + current.get_gscore(neighbor)

			# if new g_score is less than the last one, update the g_score, f_score
			# and add the node to the open_set if it does not exist or update its f_score
			# in order to be processed later
			if temp_g_score < g_score[neighbor]:
				previous_node_in_path[neighbor] = current.name
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + neighbor_node.heuristic
				if neighbor not in open_set_hash:
					open_set.update({f_score[neighbor] : neighbor_node})
					open_set_hash.add(neighbor_node)

	return False


# Parse the yaml file, create the node objects and call A*
def main():
	global path, node_dict
	# open yaml file
	graph_file = yaml.load(open(sys.argv[1], 'r'), Loader=yaml.FullLoader)
	
	nodes = []

	# parse yaml file and create nodes
	for node in graph_file['nodes']:
		if node == graph_file['start']:
			start_node = Node(node, graph_file['neighbors'][node], graph_file['heuristics'][node], graph_file['edge_cost']) 
			nodes.append(start_node)
		elif node == graph_file['goal']:
			goal_node = Node(node, graph_file['neighbors'][node], graph_file['heuristics'][node], graph_file['edge_cost'])
			nodes.append(goal_node)
		else:
			other_node = Node(node, graph_file['neighbors'][node], graph_file['heuristics'][node], graph_file['edge_cost'])
			nodes.append(other_node)
	
	# call A* and print the path if it exists
	node_dict = {node.name : node for node in nodes}
	print (path) if (a_star(nodes, start_node, goal_node)) else print("Path not found")



if __name__ == "__main__":
	main()