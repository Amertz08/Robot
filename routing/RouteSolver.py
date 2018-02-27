##################################################################################
##                                                                              ##
##   Program: Basic Route Solver for Factory Roaming Robot                      ##
##   Author: Collin Duddy                                                       ##
##   Class: EECS_542 Senior Design University of Kansas                         ##
##                                                                              ##
##   Description: This program will take in user specified input of a graph,    ##
##                or map of nodes. It will then calculate all routes possible   ##
##                from the users start node to the users end-node. This data    ##
##                will be piped to a Raspberry Pi that will then send the       ##
##                data to an arduino for roaming the map.                       ##
##################################################################################
import Graph
import argparse
import yaml
##################################################################################
##                                                                              ##
##                            Global Variables                                  ##
##                                                                              ##
##################################################################################
graph = Graph.Graph()
DIRECTIONS = ('N', 'S', 'E', 'W')
directions_dict = {}
end_node = ""
##################################################################################
##                                                                              ##
##                            Functions/Methods                                 ##
##                                                                              ##
##################################################################################

def load_config(config_file):
    global directions_dict
    '''Loads config file'''
    global graph
    with open(config_file, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    for node in cfg['nodes']:
        graph.add_vertex(node['name'])
        for connected_nodes in node['connected_nodes']:
            graph.add_edge((node['name'], connected_nodes['connected_node']))
            pair = (node,node['name'])
            directions_dict[(node['name'], connected_nodes['connected_node'])] = connected_nodes['direction']

def get_node(node_type):
    '''Gets start/end node'''
    global graph
    while True:
        node = input(f'Please enter the {node_type} node:\n')
        if node not in graph.vertices:
            print(f'Invalid {node_type} node provided.')
            print(f'Valid nodes {graph.vertices}')
            continue
        return node

def bool_input(message):
    '''Gets y/n input for given message'''
    while True:
        ans = input(f"{message} (y/n): ")
        if ans.lower() == 'y':
            return True
        elif ans.lower() == 'n':
            return False
        else:
            print(f"Invalid input: {ans} - y/n or Y/N only")

def get_graph_details_from_user():
    '''Gets graph description from user'''
    global graph
    number_of_nodes = 0
    while not number_of_nodes:
        try:
            number_of_nodes = int(input("How many nodes are in your graph? "))
        except NameError:
            print('Invalid input. Please input an integer')

    for node in range(number_of_nodes):
        new_name = input(f"Please enter a name for node {node}\n")
        graph.add_vertex(new_name)

    for node in graph.vertices:
        another_node = True
        while another_node:
            node_name = input(f"Please enter connected node name for node {node}:\n")
            if node_name in graph.vertices:
                while True:
                    direction = input(f"Please enter the cardinal direction traveling from {node} to {node_name}: {DIRECTIONS}\n")
                    if direction in DIRECTIONS:
                        graph.add_edge((node, node_name))
                        another_node = bool_input("Is there another connected node?")
                    else:
                        print(f'Invalid direction given. Valid directions ({DIRECTIONS})')
            else:
                another_node = bool_input("Invalid node name given. Is there a node connected?")

def parse_output_data(path):
    output_data = []
    for num, node in enumerate(path):
        if(num+1 is not len(path)):
            key = (node,path[num+1])
            data = (node, directions_dict[key])
            output_data.append(data)
    end_data = (end_node, '*')
    output_data.append(end_data)
    print(output_data)#This data will be sent with JSON

def main():
    '''Core app'''
    global graph
    global end_node
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help = "Optional config file to streamline graph creation.")
    parser.add_argument("-start", help = "Optional start node. If not provided user input REQUIRED")
    parser.add_argument("-end", help = "Optional end node. If not provided user input REQUIRED")
    args = parser.parse_args()
    if args.c:
        load_config(args.c)
    else:
        get_graph_details_from_user()
    if not args.start:
        start_node = get_node('start')
    else:
        start_node = args.start
    if not args.end:
        end_node = get_node('end')
    else:
        end_node = args.end
    all_paths = graph.find_all_paths(start_node, end_node)
    shortest_path = []
    for num, p in enumerate(all_paths):
        if num == 0:
            shortest_path = p;
        else:
            if len(p) < len(shortest_path):
                shortest_path = p;
    parse_output_data(shortest_path)

##################################################################################
##                                                                              ##
##                            Exeutable code below                              ##
##                                                                              ##
##################################################################################
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting...')
