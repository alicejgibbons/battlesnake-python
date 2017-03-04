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

    directions = ['up', 'down', 'left', 'right']

    ########## TESTER SNAKE ##########
    # testSnake = data['snakes']
    # testSnake.append({u'health_points': 100, u'taunt': u'92541496-7432-43c4-bed9-50584903a1f2 (20x20)', u'coords': [[2, 15], [2, 16], [2, 17]], u'name': u'battlesnake-python', u'id': u'4efdeb3d-8dd28-862a-6d139d23994f'})

    board = Board()
    
    our_snake_num, our_snake_coords = board.putSnakesOnBoard(data)

    board.putFoodOnBoard(food)
    board.printBoard(board.game_board)


    next_dir_list = findNextMove(board.game_board, our_snake_coords)
    print "next direction list is = ", next_dir_list

    dir_to_middle_list = directionToMiddle(board.game_board, our_snake_coords[0])
    print "directions to middle are = ", dir_to_middle_list

    #Just sending in the first piece of food for now.
    dir_to_food_list = directionToFood(board.game_board, our_snake_coords[0], food[0])
    print "possible directions to food are = ", dir_to_food_list

    dir_list = filterMoves(next_dir_list, dir_to_food_list)

    return {
        'move': random.choice(dir_list),
        'taunt': 'battlesnake-python!'
    }

def filterMoves(next_dir_list, dir_to_food_list):
    dirs = filter(lambda s: s in dir_to_food_list, next_dir_list)
    return dirs

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
