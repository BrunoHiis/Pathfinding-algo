from components.config import BACKGROUND, WINDOW_HEIGHT, WINDOW_WIDTH, BLOCK_SIZE, GRID_DATA, X_RANGE, Y_RANGE, SCREEN
import time
import pygame
import json

def checkIfExists(adjacentEntry, distance, nodes):
    returnable = False
    for array in nodes:
        for entry in array: 
            if adjacentEntry["x"] == entry["x"] and adjacentEntry["y"] == entry["y"]:
                if not entry["isVisited"]:
                    entry["distance"] = distance
                    adjacentEntry["distance"] = distance
                    # Need to append here
                    returnable = True
                    entry["isVisited"] = True
                    entry["isOuter"] = True
                    adjacentEntry["isVisited"] = True
                    if entry["isWall"]:
                        adjacentEntry["isWall"] = True  
                    
    return (adjacentEntry, nodes, returnable)          

def determineAdjacentNodesPositing(target, y, x, current = False):
    adjacentnodes = [target.copy(), target.copy(), target.copy(), target.copy()] if current == False else [target.copy(), target.copy(), target.copy(), target.copy(), target.copy()]
    
    adjacentnodes[0]["y"] = y + 1
    adjacentnodes[1]["x"] = x + 1
    adjacentnodes[2]["y"] = y - 1
    adjacentnodes[3]["x"] = x - 1
    
    return adjacentnodes


def getAdjacentnodes(target, nodes):
    newTarget = target.copy()
    newTarget["distance"] = newTarget["distance"] + 1
    
    adjacentnodes = determineAdjacentNodesPositing(newTarget, target["y"], target["x"])
    
    newAdjacentNodes = []
    
    for entry in adjacentnodes:
        entry, nodes, returnable = checkIfExists(entry, entry["distance"], nodes)
        # Need to append if not visited
        if returnable:
            newAdjacentNodes.append(entry)
    
    return (newAdjacentNodes, nodes)

            

def checkIfCanGo(object, nodes):
    for array in nodes:
        for entry in array: 
            if object["x"] == entry["x"] and object["y"] == entry["y"]:
                if entry["isVisited"] and not entry["isWall"]:
                        return entry["distance"]
    return False


def paintPath(object, nodes):
    for array in nodes:
        for entry in array: 
            if object["x"] == entry["x"] and object["y"] == entry["y"]:
                if entry["isFinish"]:
                    return 0
                if entry["isVisited"]:
                    nodes[entry["y"]][entry["x"]]["isPath"] = True
                    nodes[entry["y"]][entry["x"]]["isOuter"] = False
    return nodes


def getOptimalPath(start, nodes, lastpathnode):
    if lastpathnode == {}:
        newTarget = start.copy()
        y = start["y"]
        x = start["x"]
    else:
        newTarget = lastpathnode.copy()
        y = lastpathnode["y"]
        x = lastpathnode["x"]

    adjacentnodes = determineAdjacentNodesPositing(newTarget,y, x, True)

    #Determine what close by node has lowest distance
    distances = {}
    for entry in adjacentnodes:
        distance = checkIfCanGo(entry, nodes)
        if not distance == False:
            distances[distance] = entry
    
    if lastpathnode == distances[min(distances)]:
        return nodes, lastpathnode, True
    
    lastpathnode = distances[min(distances)]

    return (paintPath(lastpathnode, nodes), lastpathnode, False)
        
        
def reached_start(start, adjacentNode):
    if start["x"] == adjacentNode["x"] and start["y"] == adjacentNode["y"]:
        return True
    else:
        return False

def clean_queue(queue, nodes, distance, stop):
    # Paint outer blocks
    for array in nodes:
        for entry in array: 
            if not stop:
                if not entry["distance"] + 2 <= distance:
                    entry["isOuter"] = True
                else:
                    entry["isOuter"] = False
    
    cleanQueue = []
    
    for entry in queue:
        if not entry["distance"] + 1 <= distance:
            entry["isOuter"] = True
            cleanQueue.append(entry)
        else:
            entry["isOuter"] = False
    
    # return cleanNodes
    return cleanQueue, nodes
            
    
def path_algo(queue, nodes, stop, lastpathnode, finalStop, finishAndStartNodes):
    # Check if start and finish exist
    
    if queue == []:
        queue = [finishAndStartNodes["finish"]]
    
    queueCopy = queue.copy()
    
    # Used for optimizing
    distance = 0
    
    for entry in queueCopy:
            if not stop:
                adjacentNodes, nodes  = getAdjacentnodes(entry, nodes)
                
                for adjacentNode in adjacentNodes:
                    distance = adjacentNode["distance"]
                    if not stop:  
                        start = finishAndStartNodes["start"]
                        try:
                            isinstance(queue.index(adjacentNode), (int))
                        except ValueError as e:
                            if reached_start(start, adjacentNode):
                                stop = True
                                nodes, lastpathnode, finalStop = getOptimalPath(start, nodes, lastpathnode)
                                break
                            else:
                                if not adjacentNode["isWall"] and adjacentNode["x"] > -1 and adjacentNode["y"] > -1:
                                    queue.append(adjacentNode)
                    else:
                        break
            else:
                if not finalStop:
                    nodes, lastpathnode, finalStop = getOptimalPath(finishAndStartNodes["start"], nodes, lastpathnode)
    if not stop:
        queue, nodes = clean_queue(queue, nodes, distance, stop)

    return (queue, nodes, stop, lastpathnode, finalStop)
        
      
                            
                