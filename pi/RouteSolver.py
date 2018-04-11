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
class RouteSolver:

    def load_config(self, config_file):
        '''Loads config file'''
        with open(config_file, "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
        for node in cfg['nodes']:
            self.server_graph.add_vertex(node['name'])
            for connected_nodes in node['connected_nodes']:
                self.server_graph.add_edge((node['name'], connected_nodes['connected_node']))
                pair = (node,node['name'])
                self.directions_dict[(node['name'], connected_nodes['connected_node'])] = connected_nodes['direction']

    def parse_output_data(self, path, end_node):
        output_data = []
        for num, node in enumerate(path):
            if(num + 1 is not len(path)):
                key = (node,path[num + 1])
                data = (node, self.directions_dict[key])
                output_data.append(data)
        end_data = (end_node, '*')
        output_data.append(end_data)
        return output_data #This data will be sent with JSON

    def main(self, json_config, start_node, end_node):
        '''Core app'''
        self.load_config(json_config)
        all_paths = self.server_graph.find_all_paths(start_node, end_node)
        shortest_path = []
        for num, p in enumerate(all_paths):
            if num == 0:
                shortest_path = p;
            else:
                if len(p) < len(shortest_path):
                    shortest_path = p;
        return self.parse_output_data(shortest_path, end_node)

    def __init__(self):
        self.DIRECTIONS = ('N', 'S', 'E', 'W')
        self.directions_dict = {}
        self.server_graph = Graph.Graph()
