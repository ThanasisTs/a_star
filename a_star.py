import sys
import yaml
from ast import literal_eval

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

# Backtrack to get the path if the A* succeeds
def get_path(came_from, start, goal):
	global path
	while came_from:
		if goal not in path:
			path.append(goal)
			next_node = came_from[goal]
			del came_from[goal]
		else:

			path.append(next_node)
			try:
				next_node_key = came_from[next_node]
				del came_from[next_node]
				next_node = next_node_key
			except:
				came_from = {}
	path = path[::-1]


# A* implementation
def a_star(nodes, start, goal):
	global node_dict
	count = 0
	open_set = []
	open_set.append((0, count, start))
	came_from = {}
	
	g_score = {node.name : float("inf") for node in nodes}
	g_score[start.name] = 0

	f_score = {node.name : float("inf") for node in nodes}
	f_score[start.name] = start.heuristic

	open_set_hash = {start}

	while open_set:

		current = open_set[list(zip(*open_set))[0].index(min(list(zip(*open_set))[0]))][2]
		del open_set[list(zip(*open_set))[0].index(min(list(zip(*open_set))[0]))]

		open_set_hash.remove(current)

		if current == goal:
			get_path(came_from, start.name, goal.name)
			return True

		for neighbor in current.neighbors:
			neighbor_node = node_dict[neighbor]

			temp_g_score = g_score[current.name] + current.get_gscore(neighbor)

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current.name
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + neighbor_node.heuristic
				if neighbor not in open_set_hash:
					count += 1
					open_set.append((f_score[neighbor], count, neighbor_node))
					open_set_hash.add(neighbor_node)

	return False


# Parse the yaml file, create the node objects and call the A*
def main():
	global path, node_dict
	graph_file = yaml.load(open(sys.argv[1], 'r'), Loader=yaml.FullLoader)
	
	nodes = []

	for node in literal_eval(graph_file['nodes']):
		if node == graph_file['start']:
			start_node = Node(node, literal_eval(graph_file['neighbors'][node]), graph_file['heuristics'][node], graph_file['edge_cost']) 
			nodes.append(start_node)
		elif node == graph_file['goal']:
			goal_node = Node(node, literal_eval(graph_file['neighbors'][node]), graph_file['heuristics'][node], graph_file['edge_cost'])
			nodes.append(goal_node)
		else:
			other_node = Node(node, literal_eval(graph_file['neighbors'][node]), graph_file['heuristics'][node], graph_file['edge_cost'])
			nodes.append(other_node)
	
	node_dict = {node.name : node for node in nodes}
	print (path) if (a_star(nodes, start_node, goal_node)) else print("Path not found")



if __name__ == "__main__":
	main()