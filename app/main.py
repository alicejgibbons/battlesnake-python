import bottle
import os
import random
# ALICE, COURT, AND ROWANS SASSY SNAKE !!!!!!!!!!

class Board:

    def printBoard(self, board):
        print "BOARD STATE"
        for row in board:
            print row

    def putFoodOnBoard(self, food):
        for f in food:
            self.game_board[f[1]+1][f[0]+1] = 'f'

    def putSnakesOnBoard(self, data):
        our_id = data['you']
        snakes = data['snakes']
        snake_num = 1

        for snake in snakes:
            if snake['id'] == our_id:
                our_snake_num = snake_num
                our_snake_coords = snake['coords']
            for c in snake['coords']:
                self.game_board[c[1]+1][c[0]+1] = snake_num
            snake_num = snake_num + 1

        return our_snake_num, our_snake_coords

    def __init__(self):
        self.game_board = [[0]*22 for i in range(22)]
        self.game_board[0] = [-1] * 22
        self.game_board[21] = [-1] * 22
        for i in range(22):
            self.game_board[i][0] = -1
            self.game_board[i][21] = -1

class Coordinates:
    """
    Adjacency List implementation of a graph vertex
    We create a very simple class to represent or Graph nodes so we can use it in our Graph Traversal Algorithms
    Just the bare essentials were included here
    """
    def __init__(self, coords_id):
        """
        Constructor
        :param vert_id: The id that uniquely identifies the vertex.
        """
        self.coords_id = coords_id          # simple type
        self.neighbors = []             # type List[Vertex]
        self.status = 'undiscovered'    # undiscovered | discovered | explored

        self.distance = -1              # shortest distance from source node in shortest path search
        self.previous = []           # previous vertex in shortest path search

    def addCoords(self, coords):
        """
        Adds a new vertex as an adjacent neighbor of this vertex
        :param vertex: new Vertex() to add to self.neighbors
        """
        self.neighbors.append(coords)

    def getNeighbors(self):
        """
        Returns a list of all neighboring vertices
        :return: list of vertexes
        """
        return self.neighbors

    def getCoords(self, coords):
        # print "coords is ", coords.coords_id
        return [coords.coords_id[0],coords.coords_id[1]]


def findNextMove(board, our_snake_coords):
    our_snake_head = our_snake_coords[0]
    new_dir_list = []

    equal_list = [0, 'f']

    if board[our_snake_head[1]+2][our_snake_head[0]+1] in equal_list:
        new_dir_list.append('down')

    if board[our_snake_head[1]][our_snake_head[0]+1] in equal_list:
        new_dir_list.append('up')

    if board[our_snake_head[1]+1][our_snake_head[0]+2] in equal_list:
        new_dir_list.append('right')

    if board[our_snake_head[1]+1][our_snake_head[0]] in equal_list:
        new_dir_list.append('left')

    return new_dir_list

def directionToMiddle(board, our_snake_coords):

    dir_to_middle_list = []
    mid_coords = [9, 9]

    snake_x_coord = int(our_snake_coords[0])
    snake_y_coord = int(our_snake_coords[1])
    middl_x_coord = int(mid_coords[0])
    middl_y_coord = int(mid_coords[1])

    if snake_x_coord == middl_x_coord:
        dir_to_middle_list.append('none')

    if snake_x_coord < middl_x_coord:
        dir_to_middle_list.append('right')

    if snake_x_coord > middl_x_coord:
        dir_to_middle_list.append('left')

    if snake_y_coord == middl_y_coord:
        dir_to_middle_list.append('none')

    if snake_y_coord < middl_y_coord:
        dir_to_middle_list.append('down')

    if snake_y_coord > middl_y_coord:
        dir_to_middle_list.append('up')

    return dir_to_middle_list

def directionToFood(board, our_snake_coords, food):

    dir_to_food_list = []

    snake_x_coord = int(our_snake_coords[0])
    snake_y_coord = int(our_snake_coords[1])
    food_x_coord = int(food[0])
    food_y_coord = int(food[1])

    if snake_x_coord == food_x_coord:
        dir_to_food_list.append('none')

    if snake_x_coord < food_x_coord:
        dir_to_food_list.append('right')

    if snake_x_coord > food_x_coord:
        dir_to_food_list.append('left')

    if snake_y_coord == food_y_coord:
        dir_to_food_list.append('none')

    if snake_y_coord < food_y_coord:
        dir_to_food_list.append('down')

    if snake_y_coord > food_y_coord:
        dir_to_food_list.append('up')

    return dir_to_food_list



def shortestPathBFS(board, coords):
    """
    Shortest Path - Breadth First Search
    :param vertex: the starting graph node
    :return: does not return, changes in place
    """
    visited = []

    equal_list = [0, 'f']

    if coords is None:
        return

    queue = []                                  # our queue is a list with insert(0) as enqueue() and pop() as dequeue()
    queue.insert(0, coords)
    visited.append(coords.coords_id)

    while len(queue) > 0:
        current_coords = queue.pop()                   # remove the next node in the queue

        newCoords= current_coords.coords_id
        # newCoords = coords.getCoords(current_coords)
        #visited.append(newCoords)
        
        if board[newCoords[0]+1][newCoords[1]] in equal_list:
            newNeighbour = Coordinates([newCoords[0]+1,newCoords[1]])
            current_coords.addCoords(newNeighbour)

        if board[newCoords[0]-1][newCoords[1]] in equal_list:
            newNeighbour = Coordinates([newCoords[0]-1,newCoords[1]])
            current_coords.addCoords(newNeighbour)

        if board[newCoords[0]][newCoords[1]+1] in equal_list:
            newNeighbour = Coordinates([newCoords[0],newCoords[1]+1])
            current_coords.addCoords(newNeighbour)

        if board[newCoords[0]][newCoords[1]-1] in equal_list:
            newNeighbour = Coordinates([newCoords[0],newCoords[1]-1])
            current_coords.addCoords(newNeighbour)


        next_distance = current_coords.distance + 1     # the hypothetical distance of the neighboring node


        for neighbor in current_coords.getNeighbors():  # need to check if neighbours are -1

            foodCoords = neighbor.coords_id

            if neighbor.distance == -1 or neighbor.distance > next_distance:    # try to minimize node distance
                if neighbor.coords_id not in visited:
                    neighbor.distance = next_distance       # distance is changed only if its shorter than the current
                    neighbor.previous = current_coords    # keep a record of previous vertexes so we can traverse our path
                    # print "neighbour prev = ", neighbor.previous
                    if board[foodCoords[1]][foodCoords[0]] == 'f':
                        # print "neighbour prev", neighbor.previous.coords_id
                        # print "shortest path = ", traverseShortestPath(neighbor)
                        print "FOUND FOOD!!!!!!! WOOOOOOOO"
                        return traverseShortestPath(neighbor)
                    queue.insert(0, neighbor)
                    visited.append(neighbor.coords_id)


def traverseShortestPath(target):
    """
    Traverses backward from target vertex to source vertex, storing all encountered vertex id's
    :param target: Vertex() Our target node
    :return: A list of all vertexes in the shortest path
    """
    vertexes_in_path = []

    while target.previous:
        vertexes_in_path.append(target.coords_id)
        target = target.previous

    return vertexes_in_path

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#E579E0',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }

@bottle.post('/move')
def move():
    data = bottle.request.json
    food = data['food']

    print "data is ",data

    directions = ['up', 'down', 'left', 'right']

    ########## TESTER SNAKE ##########
    # testSnake = data['snakes']
    # testSnake.append({u'health_points': 100, u'taunt': u'92541496-7432-43c4-bed9-50584903a1f2 (20x20)', u'coords': [[2, 15], [2, 16], [2, 17]], u'name': u'battlesnake-python', u'id': u'4efdeb3d-8dd28-862a-6d139d23994f'})

    board = Board()
    
    our_snake_num, our_snake_coords = board.putSnakesOnBoard(data)

    board.putFoodOnBoard(food)
    board.printBoard(board.game_board)
    print "food is here ", food

    # BASIC ALLOWED MOVES
    next_dir_list = findNextMove(board.game_board, our_snake_coords)
    print "next direction list is = ", next_dir_list

    #dir_to_middle_list = directionToMiddle(board.game_board, our_snake_coords[0])
    #print "directions to middle are = ", dir_to_middle_list

    # BASIC SHORTEST PATH TO FOOD
    #Just sending in the first piece of food for now.
    dir_to_food_list = directionToFood(board.game_board, our_snake_coords[0], food[0])
    print "possible directions to food are = ", dir_to_food_list

    filtered_list = filterMoves(next_dir_list, dir_to_food_list)
    print "our snake coords = ", our_snake_coords

    # BFS STUFF
    our_head_coords = our_snake_coords[0]
    our_head_coords_plus_one = [our_head_coords[0]+1, our_head_coords[1]+1]

    head = Coordinates(our_head_coords_plus_one)
    print "HEAD COORDS: ", our_head_coords_plus_one

    shortest_list = shortestPathBFS(board.game_board,head)
    print "shortest list = ", shortest_list  

    if shortest_list: #shortest list not none
        new_direction = shortest_list[len(shortest_list)-1]

        new_move = 'dummy'

        print "new direction = ", new_direction

        if new_direction[0] == our_head_coords_plus_one[0]+1 and new_direction[1] == our_head_coords_plus_one[1]:
            new_move = 'right'
            print "in here right"

        if new_direction[0] == our_head_coords_plus_one[0]-1 and new_direction[1] == our_head_coords_plus_one[1]:
            new_move = 'left'
            print "in here left"

        if new_direction[0] == our_head_coords_plus_one[0] and new_direction[1] == our_head_coords_plus_one[1] +1:
            new_move = 'down'
            print "in here down"

        if new_direction[0] == our_head_coords_plus_one[0] and new_direction[1] == our_head_coords_plus_one[1] - 1:
            new_move = 'up'
            print "in here up"

        if new_move not in next_dir_list:
            print "NEW MOVE NOT IN next dir list, filtered LIST:", filtered_list
            new_move = random.choice(filtered_list)

    else:
        print "shortest list is NONE", filtered_list
        new_move = random.choice(filtered_list)
        
    return {
        'move': new_move,
        'taunt': 'battlesnake-python!'
    }

def filterMoves(next_dir_list, dir_to_food_list):
    dirs = filter(lambda s: s in dir_to_food_list, next_dir_list)
    if len(dirs) == 0:
        return next_dir_list
    return dirs

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
