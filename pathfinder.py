import pygame
import math
from components.button import button
from components.path_algo import path_algo
from components.config import BACKGROUND, WINDOW_HEIGHT, WINDOW_WIDTH, BLOCK_SIZE, GRID_DATA, X_RANGE, Y_RANGE, SCREEN
import time
import json

def main():
    nodes, finishAndStartNodes, lastpathnode, stop, finalStop, active_option, queue = initializeDefaults()
    
    pygame.init()
    pygame.display.set_caption("Path Finder")
    icon = pygame.image.load("icons/path.png")
    pygame.display.set_icon(icon)

    SCREEN.fill(BACKGROUND)
    run = True
    
    button_color = (30, 41, 59)
    button_color_active = (71, 85, 105)

    search_button = button(button_color, 0, 720, 200, 100, "Search path")
    reset_button = button(button_color, 700, 0, 100, 50, "reset")
    start_button = button(button_color, 201, 720, 200, 100, "Set start")
    end_button = button(button_color, 402, 720, 200, 100, "Set end")
    walls_button = button(button_color, 603, 720, 200, 100, "Add Walls")

    def changeColors(whitelist):
        if whitelist != "search":
            search_button.color = button_color
        if whitelist != "add_walls":
            walls_button.color = button_color
        if whitelist != "reset":
            reset_button.color = button_color
        if whitelist != "start":
            start_button.color = button_color
        if whitelist != "end":
            end_button.color = button_color
        
    last_refresh_time = 0 
    
    while run:        
        pos = pygame.mouse.get_pos()
        drawGrid(nodes)
        time_now = pygame.time.get_ticks()
        bottomRect = pygame.Rect(0, 720, 800, 800)
        pygame.draw.rect(SCREEN, (100, 116, 139), bottomRect)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONUP:
                if search_button.isOver(pos):
                    if active_option == "search":
                        search_button.color = button_color
                        active_option = ""
                    else:
                        
                        search_button.color = button_color_active
                        active_option = "search"
                        finishAndStartNodes = getFinishAndStart(nodes)
                        changeColors("search")
                        
                if walls_button.isOver(pos):
                    if active_option == "add_walls":
                        walls_button.color = button_color
                        active_option = ""
                    else:
                        walls_button.color = button_color_active
                        active_option = "add_walls"
                        changeColors("add_walls")

                if start_button.isOver(pos):
                    if active_option == "start":
                        start_button.color = button_color
                        active_option = ""
                    else:
                        start_button.color = button_color_active
                        active_option = "start"
                        changeColors("start")

                if end_button.isOver(pos):
                    if active_option == "end":
                        end_button.color = button_color
                        active_option = ""
                    else:
                        end_button.color = button_color_active
                        active_option = "end"
                        changeColors("end")
                if reset_button.isOver(pos):
                    if active_option == "reset":
                        reset_button.color = button_color
                        active_option = ""
                    else:
                        reset_button.color = button_color_active
                        active_option = "reset"
                        changeColors("reset")

            if pygame.mouse.get_pressed()[0]:
                try:
                    if active_option == "add_walls":
                        nodes = addWalls(pos, nodes)
                except AttributeError:
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                if active_option == "start":
                    nodes = setStart(pos, nodes)
                elif active_option == "end":
                    nodes = setEnd(pos, nodes)
                elif active_option == "reset":
                    response = reset(pos)
                    if response:
                        nodes, finishAndStartNodes, lastpathnode, stop, finalStop, active_option, queue = response
                    break

        
        # print(time_now)
        if active_option == "search":
            if finalStop == True:
                active_option = ""
            else:
                if finishAndStartNodes["start"] and finishAndStartNodes["finish"]:
                    queue, nodes, stop, lastpathnode, finalStop = path_algo(queue, nodes, stop, lastpathnode, finalStop, finishAndStartNodes)
                else:
                    active_option = ""

        search_button.draw(SCREEN)
        reset_button.draw(SCREEN)
        start_button.draw(SCREEN)
        end_button.draw(SCREEN)
        walls_button.draw(SCREEN)
        pygame.display.update()
        last_refresh_time = time_now
        
        
def getFinishAndStart(nodes):
    start = {}
    finish = {}
    
    for array in nodes:
        for entry in array:
            if entry["isStart"]:
                start = entry
            elif entry["isFinish"]:
                finish = entry
    
    return {"start": start, "finish": finish}

def positionClicked(cursor_pos):
    x = cursor_pos[0] / BLOCK_SIZE
    y = cursor_pos[1] / BLOCK_SIZE

    # Check if click is on grid
    if (x < X_RANGE) and (y < Y_RANGE):
        return True
    else:
        return False

def addWalls(pos, nodes):
    if positionClicked(pos):
        nodes[math.floor(pos[1] / BLOCK_SIZE)][math.floor(pos[0] / BLOCK_SIZE)]["isWall"] = True
        return nodes
    else:
        return nodes
    
def reset(cursor_pos):
    x = cursor_pos[0] / BLOCK_SIZE
    y = (cursor_pos[1]) / BLOCK_SIZE
    
    # Check if click is on grid
    if (x < X_RANGE) and (y < Y_RANGE):
        return initializeDefaults()
        
def initializeDefaults():
    nodes = []
    lastpathnode = {}
    stop = False
    finalStop = False
    finishAndStartNodes = {}

    for y in range(Y_RANGE):
        currentRow = []
        for x in range(X_RANGE):
            currentNode = {
                "y": y,
                "x": x,
                "isVisited": False,
                "isStart": False,
                "isPath": False,
                "isFinish": False,
                "isWall": False,
                "isOuter": False,
                "previousNode": None,
                "new": None,
                "distance": 0
            }
            currentRow.append(currentNode)
        nodes.append(currentRow)
    active_option = ""
    queue = []

    return (nodes, finishAndStartNodes, lastpathnode, stop, finalStop, active_option, queue)



def setStart(pos, nodes):
    if positionClicked(pos):
        clickedNode = nodes[math.floor(pos[1] / BLOCK_SIZE)][math.floor(pos[0] / BLOCK_SIZE)]
        if clickedNode["isStart"]:
            clickedNode["isStart"] = False
        else:
            clickedNode["isStart"] = True
            clickedNode["isFinish"] = False
            clickedNode["isWall"] = False
            clickedNode["isVisited"] = False
    return nodes

def setEnd(pos, nodes):
    if positionClicked(pos):
        clickedNode = nodes[math.floor(pos[1] / BLOCK_SIZE)][math.floor(pos[0] / BLOCK_SIZE)]
        if clickedNode["isFinish"]:
            clickedNode["isFinish"] = False
        else:
            clickedNode["isFinish"] = True
            clickedNode["isStart"] = False
            clickedNode["isWall"] = False
            clickedNode["isVisited"] = False
        return nodes
    else:
        return nodes

# Text has been disabled for pygame performance issues

def text_to_screen(screen, text, x, y, size = 30,
    color = (109, 117, 122)):
    text = str(text)
    font = pygame.font.SysFont('arial', 10)
    text = font.render(text, True, color)
    screen.blit(text, (x*BLOCK_SIZE + 2 +3, y * BLOCK_SIZE + 2 +1))
   

def drawGrid(nodes):
        
    for x in range(X_RANGE):
        for y in range(Y_RANGE):
            rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE,
                               BLOCK_SIZE, BLOCK_SIZE)
            if nodes[y][x]["isWall"]:
                pygame.draw.rect(SCREEN, (71, 85, 105), rect)
            elif nodes[y][x]["isStart"]:
                pygame.draw.rect(SCREEN, (37, 99, 235), rect)
                # text_to_screen(SCREEN, nodes[y][x]["distance"], x, y, 30, (219, 234, 254))
            elif nodes[y][x]["isFinish"]:
                pygame.draw.rect(SCREEN, (239, 68, 68), rect)
                # text_to_screen(SCREEN, nodes[y][x]["distance"], x, y, 30, (219, 234, 254))
            elif nodes[y][x]["isOuter"]:
                pygame.draw.rect(SCREEN, (226, 232, 240), rect)
                pygame.draw.rect(SCREEN, (255, 255, 255), rect, 1,1)
                # text_to_screen(SCREEN, nodes[y][x]["distance"], x, y)
            elif nodes[y][x]["isPath"]:
                pygame.draw.rect(SCREEN, (74, 222, 128), rect)
                # text_to_screen(SCREEN, nodes[y][x]["distance"], x, y, 30, (187, 247, 208))
            elif nodes[y][x]["isVisited"]:
                pygame.draw.rect(SCREEN, (203, 213, 225, 0.1), rect)
                pygame.draw.rect(SCREEN, (255, 255, 255), rect, 1,1)
                # text_to_screen(SCREEN, nodes[y][x]["distance"], x, y)
            else:
                pygame.draw.rect(SCREEN, (241, 245, 249), rect)
                pygame.draw.rect(SCREEN, (255, 255, 255), rect, 1,3)
  
    return nodes

# Only when run as a script
if __name__ == "__main__":
    main()
