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
import sys
import re
##################################################################################
##                                                                              ##
##                            Global Variables                                  ##
##                                                                              ##
##################################################################################
graph = Graph.Graph()
##################################################################################
##                                                                              ##
##                            Functions/Methods                                 ##
##                                                                              ##
##################################################################################

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def loadConfig(configFile):
    f = open(configFile,"r")
    lines = f.readlines()
    currNode = ""
    bad_chars = '(){}<>[]'
    for i in range(0,len(lines)):
        line= lines[i]
        if "Next Node:" in line:
            graph.add_vertex(lines[i+1].strip())
            currNode = lines[i+1].strip()
        elif "Connected Nodes:" in line:
            connectedNodes = lines[i+1].split(';')
            for node in connectedNodes:
                nodeName = node.split(',')
                for c in bad_chars: nodeName[0] = nodeName[0].replace(c, "")
                for c in bad_chars: nodeName[1] = nodeName[1].replace(c, "")
                nodeName[1].rstrip()
                #graph.add_edge((currNode,(nodeName[0],nodeName[1])))
                # Adding directions is causing an issue. May have to come up with
                #another solution for direction
                graph.add_edge((currNode,nodeName[0]))

def getGraphDetailsFromUser():
    numberOfNodes = 0;
    while True:
        numberOfNodes = input("How many nodes are in your graph? ")
        if(is_int(numberOfNodes)):
            break
    nodeCount = 0
    while (nodeCount < int(numberOfNodes)):
        newName = input("Please enter a name for node {}\n".format(nodeCount))
        graph.add_vertex(newName)
        nodeCount += 1
    print(graph.vertices())
    for node in graph.vertices():
        anotherNode = True
        while anotherNode:
            nodeName = input("Please enter connected node name for node {}:\n".format(node))
            if(nodeName in graph.vertices()):
                while True:
                    direction = input("Please enter the cardinal direction traveling from {} to {}: (N E S W)\n".format( node, nodeName))
                    if direction is "N" or "S" or "E" or "W":
                        graph.add_edge((node,nodeName))
                        anotherConnection = input("Is there another connected node? (y/n)\n")
                        if(anotherConnection == 'n'):
                            anotherNode = False
                        elif(anotherConnection == 'y'):
                            #do nothing
                            anotherNode = True
                        else:
                            while True:
                                print("Invalid Input Given.")
                                anotherConnection = input("Is there another connected node? (y/n)\n")
                                if(anotherConnection == 'n'):
                                    anotherNode = False
                                elif(config == 'y'):
                                    break
                        break
                    else:
                        print("Invalid direction given. Please enter N, E, S, or W")
            else:
                connected = input("Invalid node name given. Is there a node connected? (y/n)\n")
                if(connected == 'n'):
                    anotherNode = False
                elif(connected == 'y'):
                    anotherNode = True

def main(argv):
    if len(argv)>0:
        loadConfig(argv[0])
    else:
        getGraphDetailsFromUser()
    while True:
        startNode = input("Please enter the start node:\n")
        if(startNode in graph.vertices()):
            break;
        else:
            print("Invalid start node provided\n")
    while True:
        endNode = input("Please enter the end node:\n")
        if(startNode in graph.vertices()):
            break;
        else:
            print("Invalid end node provided\n")
    paths = graph.find_path(startNode,endNode)
    print("This is a single path: ")
    print(paths)
    allPaths = graph.find_all_paths(startNode,endNode)
    print("These are all possible paths: ")
    print(allPaths)
    for p in allPaths:
        print(p)

##################################################################################
##                                                                              ##
##                            Exeutable code below                              ##
##                                                                              ##
##################################################################################
if __name__ == "__main__":
	main(sys.argv[1:])
