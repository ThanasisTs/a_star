import sys
import yaml
from ast import literal_eval



graph_file = yaml.load(open(sys.argv[1], 'r'), Loader=yaml.FullLoader)


print(type(graph_file['nodes']))

