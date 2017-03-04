import bottle
import os
import random
# ALICE, COURT, AND ROWANS SASSY SNAKE !!!!!!!!!!

class Board:
    def putFoodOnBoard(self, food):
        for f in food:
            self.game_board[f[1]][f[0]] = 'f'

    def updateBoard(self, coords):
        for c in coords:
            self.game_board[c[1]][c[0]] = 1

    def __init__(self):
        self.game_board = [[0]*22 for i in range(22)]
        self.game_board[0] = [-1] * 22
        self.game_board[21] = [-1] * 22
        for i in range(22):
            self.game_board[i][0] = -1
            self.game_board[i][21] = -1


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

    me_snake = idCheck(data)

    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']

    print "SNAKES"
    snakes = data['snakes']
    our_snake = snakes[0]
    coords = our_snake['coords']
    print coords
    
    print "SNAKE FOOD"
    food = data['food']
    print food

    board = Board()
    #printBoard(board.game_board)
    
    board.updateBoard(coords)
    printBoard(board.game_board)

    board.putFoodOnBoard(food)
    printBoard(board.game_board)

    return {
        'move': 'up',
        'taunt': 'battlesnake-python!'
    }

def idCheck(data):
    our_id = data['you']
    snakes = data['snakes']

    for snake in snakes:
        if snake['id'] == our_id:
            return {
                'ignore_me': snake
            }

def printBoard(board):
    print "BOARD STATE"
    for row in board:
        print row


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
