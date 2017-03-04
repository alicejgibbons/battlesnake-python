import bottle
import os
import random
# ALICE, COURT, AND ROWANS SASSY SNAKE !!!!!!!!!!

class Board:
    def updateBoard(self, coords, snake_num):
        for c in coords:
            self.game_board[c[1]][c[0]] = snake_num

    def putSnakesOnBoard(self, data, board):
        our_id = data['you']
        snakes = data['snakes']
        snake_num = 1

        for snake in snakes:
            if snake['id'] == our_id:
                our_snake_num = snake_num
            board.updateBoard(snake['coords'], snake_num)
            snake_num = snake_num + 1

        return our_snake_num, board

    def __init__(self):
        self.game_board = [[0]*20 for i in range(20)]




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

    directions = ['up', 'down', 'left', 'right']

    ########## TESTER SNAKE ##########
    # testSnake = data['snakes']
    # testSnake.append({u'health_points': 100, u'taunt': u'92541496-7432-43c4-bed9-50584903a1f2 (20x20)', u'coords': [[2, 15], [2, 16], [2, 17]], u'name': u'battlesnake-python', u'id': u'4efdeb3d-8dd28-862a-6d139d23994f'})

    board = Board()
    printBoard(board.game_board)
    
    our_snake_num, newBoard = board.putSnakesOnBoard(data, board)

    printBoard(newBoard.game_board)


    return {
        'move': 'up',
        'taunt': 'battlesnake-python!'
    }

def printBoard(board):
    print "BOARD STATE"
    for row in board:
        print row


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
