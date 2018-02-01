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
##################################################################################
##                                                                              ##
##                            Functions/Methods                                 ##
##                                                                              ##
##################################################################################

def load_config(config_file):
    '''Loads config file'''
    global graph
    with open(config_file, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    for node in cfg['nodes']:
        graph.add_vertex(node['name'])
        for connected_nodes in node['connected_nodes']:
            graph.add_edge((node['name'], connected_nodes['connected_node']))
            #Add directional support here

def get_node(node_type):
    '''Gets start/end node'''
    global graph
    while True:
        node = input(f'Please enter the {node_type} node:\n')
        if node not in graph.vertices:
            print(f'Invalid {node_type} node provided\n')
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

    print(graph.vertices)
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

def main():
    '''Core app'''
    global graph
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="Optional config file to streamline graph creation.")
    args = parser.parse_args()
    if args.c:
        load_config(args.c)
    else:
        get_graph_details_from_user()
    start_node = get_node('start')
    end_node = get_node('end')
    paths = graph.find_path(start_node, end_node)
    print("This is a single path: ")
    print(paths)
    all_paths = graph.find_all_paths(start_node, end_node)
    print("These are all possible paths: ")
    print(all_paths)
    for p in all_paths:
        print(p)

##################################################################################
##                                                                              ##
##                            Exeutable code below                              ##
##                                                                              ##
##################################################################################
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting...')
