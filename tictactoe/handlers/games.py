import logging
import uuid
import tornado.web
import json
import hashlib

from tornado import gen
from tictactoe.model.game import get_game_payload
from tictactoe.handlers.base import BaseHandler
logger = logging.getLogger(__name__)
games = {}


class GameLogic(Object):
    def get_winner(cls,board_data):
        # check left diagonal
        point = board_data[0,0] + board_data[1,1] + board_data[2,2]
        if point == 3:
            return 'X'
        if point == -3:
            return 'O'
        # check right diagonal
        point = board_data[0,2] + board_data[1,1] + board_data[2,0]
        if point == 3:
            return 'X'
        if point == -3:
            return 'O'
        # check point horizontal
        point = board_data[0,0] + board_data[0,1] + board_data[0,2]
        if point == 3:
            return 'X'
        if point == -3:
            return 'O'
        point = board_data[1,0] + board_data[1,1] + board_data[1,2]
        if point == 3:
            return 'X'
        if point == -3:
            return 'O'
        point = board_data[2,0] + board_data[2,1] + board_data[2,2]
        if point == 3:
            return 'X'
        if point == -3:
            return 'O'
        # chekc point vertically
        point = board_data[0,0] + board_data[1,0] + board_data[2,0]
        if point == 3:
            return 'X'
        if point == -3:
            return 'O'
        point = board_data[0,1] + board_data[1,1] + board_data[2,1]
        if point == 3:
            return 'X'
        if point == -3:
            return 'O'
        point = board_data[0,2] + board_data[1,2] + board_data[2,2]
        if point == 3:
            return 'X'
        if point == -3:
            return 'O'
        
    def validateMove(board_data,x,y):
        if board_data[x][y] == 0:
            return True
        else:
            return False

class GamesHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        response = {
            "status":"ok",
            "result":games
        }
        self.write(response) 
        
    @gen.coroutine
    def post(self):
        game = get_game_payload()
        m = hashlib.md5()
        m.update(str(uuid.uuid4()))
        g_id = m.hexdigest()
        games[g_id] = game
        response = {
            "status":"ok",
            "type":"post",
            "result":{
                "g_id": g_id       
            }
        }
        self.write(response) 

class GamesPropertiesHandler(BaseHandler):
    @gen.coroutine
    def get(self, token):
        logger.info(token)
        if not token:
            self.send_error(status_code=400)
            return
        game_data = games[token]
        response = {
            "status":"ok",
            "type":"get",
            "result":game_data
        }
        self.write(response) 
        
    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body)
        logger.info("game users details", data.player)
        logger.info("game move  details", data.board.x)
        logger.info("game move  details", data.board.y)
        """
        Draft
        First check if game has 2 players if yes ask for game moves 
        then check if its that users turn 
        then make the move and check if user won?
        if yes respond with winner name and game board matric 
            
            generic response should be game board 
            player name whose move is next
            winner name 
            
            game board description 
            0  - null value
            1  - represents X
            -1 - represents O
        """
        games.append(data.get("name"))
        response = {
            "status":"ok",
            "type":"post",
            "result":{
                "winner":""
                "game_board":[[],[],[]],
                "move":         
            }
        }
        self.write(response) 
        

        
        

        
