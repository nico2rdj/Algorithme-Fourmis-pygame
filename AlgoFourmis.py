import sys, math, random
import pygame
import pygame.draw
import numpy as np

__screenSize__ = (1280,1280) #(1280,1280)
__cellSize__ = 40
__gridDim__ = tuple(map(lambda x: int(x/__cellSize__), __screenSize__))

__colors__ = [(255,255,255),(0,120,0),(255,10,10),(128,128,128),(255,255,0)]

def getColorCell(n):
    return __colors__[n]

def _getColorCell(node):
    if node is None:
        return __colors__[0]
    return __colors__[1]

class Edge:
    def __init__(self, node_1, node_2, weight, initial_pheromone):
        self.node_1 = node_1
        self.node_2 = node_2
        self.weight = weight
        self.pheromone = initial_pheromone

class Node:
    def __init__(self, name, coordX, coordY):
        self.name = name
        self.coordX = coordX
        self.coordY = coordY

class Ant:
    def __init__(self, alpha, beta, nodes, edges):           
        self.alpha = alpha
        self.beta = beta
        self.nodes = nodes
        self.edges = edges
        self.path = []
        self.current_node = nodes[0]
        self.visited_nodes = [nodes[0]]

    def get_distance(self):
        distance = 0
        for i in range(len(path)):
            distance += path[i].weight
        return distance

    def unvisited_edges(self):
        unvisited_tab = []
        for edge in self.edges:
            if edge.node_1 == self.current_node and edge.node_2 not in self.visited_nodes:
                unvisited_tab.append(edge)
        return unvisited_tab

    def next_node(self):
        
        unvisited_edges = self.unvisited_edges()
        move_values = []

        for edge in unvisited_edges:
            move_value = (edge.pheromone ** self.alpha) + ((1.0/edge.weight)**self.beta)
            move_values.append(move_value)
        move_values = move_values / sum(move_values)
        move = np.random.choice(len(move_values),1,p=move_values)[0]
        return unvisited_edges[move]
    
    def get_last_edge(self):
        
        for edge in self.edges:
            if edge.node_1.name == self.current_node.name and edge.node_2.name == self.nodes[0].name:
                return edge

    def run(self):
        while len(self.visited_nodes) < len(self.nodes):

            next_edge = self.next_node()
            self.current_node = next_edge.node_2
            self.visited_nodes.append(self.current_node)
            self.path.append(next_edge)
        
        # add the last edge that link the beggining
        last_edge = self.get_last_edge()
        self.path.append(last_edge)

        return self.path
            





class Grid:
    _grid= None
    _gridbis = None
    _indexVoisins = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    # edges_matrix: edges cost between nodes
    # nodes_coord: nodes coordinate
    def __init__(self, edges_matrix=None, nodes_coord=None):
        print("Creating a grid of dimensions " + str(__gridDim__))
        # initialize the grid
        self._grid = np.zeros(__gridDim__, dtype=Node)
        self._gridbis = np.zeros(__gridDim__, dtype=Node)

        # initialize nodes in the grid
        
        for (x,y) in np.ndindex(__gridDim__):
            self._grid[x,y] = None

        num_node = 0
        for (x,y) in nodes_coord:
            self._grid[x,y] = Node(num_node, x, y)
            num_node += 1



class Scene:
    _mouseCoords = (0,0)
    _grid = None
    _font = None

    def __init__(self, colony_size=100, alpha=1, beta=2, decay=0.5, initial_pheromone=0.0):
        pygame.init()
        self._screen = pygame.display.set_mode(__screenSize__)
        self._font = pygame.font.SysFont('Arial',25)
        self.nodes_coord = [(4,2), (12,2), (16,12), (12,16), (4,8)]
        self.edges_matrix = np.array([
                                     [0,10,20,30,15]
                                    ,[10,0,10,20,25]
                                    ,[20,10,0,10,20]
                                    ,[30,20,10,0,10]
                                    ,[15,25,20,10,0]
                                    ])
        self._grid = Grid(nodes_coord=self.nodes_coord)

        self.colony_size = colony_size
        self.alpha = alpha
        self.beta = beta
        self.initial_pheromone = initial_pheromone
        self.decay = decay


        self.nodes = self.create_nodes()
        self.edges = self.create_edges()
        self.ant_colony = self.create_ant_colony()

        #self._grid.tickMecontents()
    
    def create_nodes(self):
        nodes_tab = []
        node_name = "A"
        for node in self.nodes_coord:
            new_node = Node(node_name, node[0], node[1])
            nodes_tab.append(new_node)
            node_name = chr(ord(node_name) + 1)
        return nodes_tab


    def create_edges(self):
        edges_tab = []
        first_node = 0
        for edges in self.edges_matrix:
            second_node = 0
            for edge in edges:
                if edge != 0:
                    new_edge = Edge(self.nodes[first_node], self.nodes[second_node], edge, self.initial_pheromone * self.decay)
                    edges_tab.append(new_edge)
                second_node += 1
            first_node += 1
        return edges_tab
                    

    def create_ant_colony(self):
        ant_tab = []
        for i in range(self.colony_size):
            new_ant = Ant(self.alpha, self.beta, self.nodes, self.edges)
            ant_tab.append(new_ant)
        return ant_tab

    def get_all_paths(self):
        all_paths = []
        for ant in self.ant_colony:
            all_paths.append(ant.path)
        return all_paths

    def get_distance(self, path):
        distance = 0
        for i in range(len(path)):
            distance += path[i].weight
        return distance

    def set_decay(self):
        for edge in self.edges:
            edge.pheromone *= self.decay

    def get_pheromone(self, path):
        pheromone = 0
        for i in range(len(path)):
            pheromone += path[i].pheromone
        return pheromone

    def spread_pheromone(self, all_paths):
        for path in all_paths:
            for edge in path:
                edge.pheromone += 1.0 / self.get_distance(path)

    def get_heavier_path(self, all_paths):
        max_dist = self.get_pheromone(all_paths[0])
        heavier_path = all_paths[0]
        for path in all_paths[1:]:
            if self.get_pheromone(path) > max_dist:
                heavier_path = path
        return heavier_path

    def print_path(self, path):
        for edge in path:
            print(edge.node_1.name + "-->" + edge.node_2.name)
            print(str(edge.pheromone))

        print("#################################")

    def run_ant_colony(self):
        self.ant_colony = self.create_ant_colony()
        for ant in self.ant_colony:
            ant.run()
        all_paths = self.get_all_paths()
        self.set_decay()
        self.spread_pheromone(all_paths)
        self.print_path(self.get_heavier_path(all_paths))

        
        




        


    # draw the nodes and link between them
    def drawMe(self):


        if self._grid._grid is None:
            return
        self._screen.fill((255,255,255))
        
        # Initialize the font system and create the font and font renderer
        pygame.font.init()
        default_font = pygame.font.get_default_font()
        font_renderer = pygame.font.Font(default_font, 12)


        # draw the edges
        for edge in self.edges:
            first_node = edge.node_1
            second_node = edge.node_2

            x_first = first_node.coordX * (__cellSize__+1) + __cellSize__ // 2
            y_first = first_node.coordY * (__cellSize__+1) + __cellSize__ // 2
            x_second = second_node.coordX * (__cellSize__+1) + __cellSize__ // 2
            y_second = second_node.coordY * (__cellSize__+1) + __cellSize__ // 2

            pygame.draw.line(self._screen, (120, 120, 120), (x_first,y_first), (x_second,y_second))

            label = font_renderer.render(str(edge.weight), 1, (0,0,0)) 
            self._screen.blit(label, ((x_first + x_second)//2,(y_first + y_second)//2))  

        all_paths = self.get_all_paths()
        h_path = self.get_heavier_path(all_paths)
        for edge in h_path:
            first_node = edge.node_1
            second_node = edge.node_2

            x_first = first_node.coordX * (__cellSize__+1) + __cellSize__ // 2
            y_first = first_node.coordY * (__cellSize__+1) + __cellSize__ // 2
            x_second = second_node.coordX * (__cellSize__+1) + __cellSize__ // 2
            y_second = second_node.coordY * (__cellSize__+1) + __cellSize__ // 2

            pygame.draw.line(self._screen, (200, 0, 0), (x_first,y_first), (x_second,y_second), 5)

            label = font_renderer.render(str(edge.pheromone), 1, (0,0,0)) 
            self._screen.blit(label, ((x_first + x_second)//2+30,(y_first + y_second)//2))  


        # draw the nodes
        font_renderer = pygame.font.Font(default_font, 15)
        
        for node in self.nodes:
            x = node.coordX
            y = node.coordY
            pygame.draw.circle(self._screen, 
                    _getColorCell(self._grid._grid.item((x,y))),
                    (x*__cellSize__ + 1 + __cellSize__ // 2, y*__cellSize__ + 1 + __cellSize__ // 2), __cellSize__ // 2)
            
            
            # write the node name
            label = font_renderer.render(node.name, 1, (255,255,255)) 
            self._screen.blit(label, (x*__cellSize__ + 1 + __cellSize__ // 3, y*__cellSize__ + 1 + __cellSize__ // 3))

              
    
       
            
        

       

        



            
            

        



    def drawText(self, text, position, color = (255,64,64)):
        self._screen.blit(self._font.render(text,1,color),position)

    def update(self):
        pass

    def eventClic(self,coord,b): # ICI METTRE UN A* EN TEMPS REEL
        pass
    def recordMouseMove(self, coord):
        pass

def main():
    buildingGrid = False # True if the user can add / remove walls / weights
    scene = Scene()
    done = False
    clock = pygame.time.Clock()
    buildingTrack = True
    wallWeight = 1
    while done == False:
        #scene._grid.tickMecontents()
        #scene._grid._grid = np.copy(scene._grid._gridbis)
        clock.tick(10)
        scene.run_ant_colony()
        scene.drawMe()
        pygame.display.flip()
        #scene._grid.tickMoves()
        #scene._grid._grid = np.copy(scene._grid._gridbis)
        clock.tick(10)
        scene.drawMe()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                print("Exiting")
                done=True

    pygame.quit()

if not sys.flags.interactive: main()

