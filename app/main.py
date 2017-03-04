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

def bfs(board, start):
    visited, queue = [], [start]
    while queue:
        vertex = queue.pop(0)
        print "popped from queue = board[",vertex[0],"][",vertex[1],"]"
        vertex_value = board[vertex[0]][vertex[1]]
        print "vertex_value = ", vertex_value
        if vertex_value == 'f':
            return visited
        if vertex not in visited and vertex_value == 0:
            visited.append(vertex)
            vertex_list = [[vertex[0]+1,vertex[1]], [vertex[0]-1,vertex[1]], [vertex[0],vertex[1]+1], [vertex[0],vertex[1]-1]]
            for child in vertex_list:
                if child not in visited:
                    queue.append(child)
            
            #queue.extend(board[vertex] - visited)

    return visited


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
        'color': '#00FF00',
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
    # board.printBoard(board.game_board)

    next_dir_list = findNextMove(board.game_board, our_snake_coords)
    print "next direction list is = ", next_dir_list

    print "our snake coords = ", our_snake_coords

    our_head_coords = our_snake_coords[0]

    up_list = []
    down_list = []
    right_list =[]
    left_list = []

    lists = { 'up': None, 'down': None, 'right': None, 'left': None}
    shortest_list = {'move':None, 'l':None}
    for i in range(len(next_dir_list)):
        if 'up' in next_dir_list:
            lists['up'] = bfs(board.game_board, [our_head_coords[0]+2, our_head_coords[1]+1])
            shortest_list['move'] = 'up'
            shortest_list['l'] = lists['up']
        if 'down' in next_dir_list:
            lists['down'] = bfs(board.game_board, [our_head_coords[0], our_head_coords[1]+1])
            shortest_list['move'] = 'down'
            shortest_list['l'] = lists['down']
        if 'right' in next_dir_list:
            lists['right'] = bfs(board.game_board, [our_head_coords[0]+1, our_head_coords[1]+2])
            shortest_list['move'] = 'right'
            shortest_list['l'] = lists['right']
        if 'left' in next_dir_list:
            lists['left'] = bfs(board.game_board, [our_head_coords[0]+1, our_head_coords[1]])
            shortest_list['move'] = 'left'
            shortest_list['l'] = lists['left']
    
    print "len up list = ", lists['up']
    print "len down list = ", lists['down']
    print "len right_list list = ", lists['right']
    print "len left list = ",  lists['left'] 

    for k,v in lists.iteritems():
        #print len(v) 
        if v and len(v) < len(shortest_list['l']):
            print "LIST: ", k, len(v)
            shortest_list['move'] = k
            shortest_list['l'] = v
            #print shortest_list
    #print shortest_list
    print "shortest_list LENGTH:",  len(shortest_list['l'])
    print "shortest_list MOVE",  shortest_list['move']


    return {
        'move': shortest_list['move'],
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
