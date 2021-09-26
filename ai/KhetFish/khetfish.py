import numpy as np
import pygame.event
from tqdm import tqdm
from ai.actions import convert_to_readable, is_terminal, possible_actions_4_state, apply_move, deepcopy, mirror_state, apply_move_visuals
from ai.globals import *
#from game import make_grid, refresh_display, sys
import uuid
from multiprocessing import Pool, cpu_count


class Game:
    def __init__(self,evalulate_position = None):
        if evalulate_position is not None:
            self.evaluate_position = evalulate_position

    # TODO: better evaluation
    def evaluate_position(self,board,player):
        pos_score = 0
        for i in range(8):
            for j in range(10):
                piece = board[i][j]
                if piece != 0 and piece.type != 'dj':
                    if piece.team == player:
                        pos_score += piece.value
                    elif piece.team != player:
                        pos_score -= piece.value
        return pos_score

    # TODO: make faster
    def valid_moves(self,board,player):
        return possible_actions_4_state(board,player)

    # TODO: make faster
    def get_next_board(self,board,move,player):
        try: return apply_move(move,board,player)
        except Exception as e:
            valids = self.valid_moves(board,player)
            print(move)
            print(move in valids)
            print(player)
            self.display(board)
            self.display(mirror_state(board))
            raise e

    def isTerminal(self, board,player):
        return is_terminal(board,player)

    def reverse_player(self,player):
        if player == 's':
            return 'r'
        else:
            return 's'

    def mm(self,move, board,depth,isMaximizing,player):
        board = self.get_next_board(board,move,player)
        value = self.minimax(depth - 1, board, -np.inf, np.inf, not isMaximizing, player)
        return [value, move]

    def mmWrapper(self,args):
        return self.mm(*args)


    def minimaxRoot(self, depth, board, isMaximizing,player):
        possibleMoves = self.valid_moves(board,player)
        bestMove = -np.inf
        bestMoveFinal = None

        args = [(move,board,depth,isMaximizing,player) for move in possibleMoves]

        threads = cpu_count()
        with Pool(threads) as p:
            bestMoveList = np.array(list(tqdm(p.imap(self.mmWrapper, args), total=len(args))))
        return bestMoveList[:,1][np.argmax(bestMoveList[:,0])]
        """
        for x in tqdm(possibleMoves):
            move = x
            old_board = deepcopy(board)
            board = self.get_next_board(board, move, player)
            value = np.maximum(bestMove, self.minimax(depth - 1, board, -np.inf, np.inf, not isMaximizing,player))
            board = old_board
            if (value > bestMove):
                #print("Best score: ", str(bestMove))
                #print("Best move: ", str(bestMoveFinal))
                bestMove = value
                bestMoveFinal = move
        return bestMoveFinal
        """

    def minimax(self,depth, board, alpha, beta, is_maximizing, player):
        if not is_maximizing:
            player = self.reverse_player(player)

        if (depth == 0) or self.isTerminal(board,player):
            return self.evaluate_position(board,player)

        possibleMoves = self.valid_moves(board,player)
        if (is_maximizing):
            bestMove = -np.inf
            for x in possibleMoves:
                move = x
                old_board = deepcopy(board)
                board = self.get_next_board(board,move,player)
                bestMove = max(bestMove, self.minimax(depth - 1, board, alpha, beta, not is_maximizing,player))
                board = old_board
                alpha = np.maximum(alpha, bestMove)
                if beta <= alpha:
                    return bestMove
            return bestMove
        else:
            bestMove = np.inf
            for x in possibleMoves:
                move = x
                old_board = deepcopy(board)
                board = self.get_next_board(board, move,player)

                bestMove = min(bestMove, self.minimax(depth - 1, board, alpha, beta, not is_maximizing,player))
                board = old_board
                beta = np.minimum(beta, bestMove)
                if (beta <= alpha):
                    return bestMove
            return bestMove

    def display(self,board):
        print(convert_to_readable(board))




def playGame(depth):
    game = Game()
    board = classic_board
    #game.display(board)
    player = 's'
    move_n = 1
    file_id = str(uuid.uuid4().hex)+'.txt'
    while not game.isTerminal(board,player):
        best = game.minimaxRoot(depth, board, True, player)
        new_board = game.get_next_board(board, best, 's')
        player = game.reverse_player(player)
        board = new_board

        open(file_id,'a').write(best+'\n')
        #game.display(board)
        if move_n == 100:
            open(file_id, 'a').write('DRAW')
            return
        move_n+=1
    open(file_id,'a').write('WIN/LOSS')
    #game.display(board)
    return


if __name__ == '__main__':
    playGame(3)


