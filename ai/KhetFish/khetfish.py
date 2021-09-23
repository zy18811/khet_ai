import numpy as np
from tqdm import tqdm
from ai.piece_init import *
from ai.actions import convert_to_readable, is_terminal, possible_actions_4_state, apply_move, deepcopy, mirror_state


class Game:
    def __init__(self,evalulate_position = None):
        if evalulate_position is not None:
            self.evaluate_position = evalulate_position

    def evaluate_position(self,board,player):
        pos_score = 0
        for i in range(8):
            for j in range(10):
                piece = board[i][j]
                if piece != 0 and piece.type != 'dj':
                    if piece.team == player:
                        pos_score += piece.value
                    elif piece.team == player:
                        pos_score -= piece.value
        return pos_score

    def valid_moves(self,board,player):
        return possible_actions_4_state(board,player)

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

    def minimaxRoot(self, depth, board, isMaximizing,player):
        possibleMoves = self.valid_moves(board,player)
        bestMove = -np.inf
        bestMoveFinal = None
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


    def minimax(self,depth, board, alpha, beta, is_maximizing, player):
        if not is_maximizing:
            player = self.reverse_player(player)

        if (depth == 0):
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

def is_over(board):
    if np.isin(board,[spha,rpha],invert=True).any():
        return False
    else: return True


def playGame(depth):
    game = Game()
    board = classic_board
    game.display(board)
    player = 's'
    while not is_over(board):
        best = game.minimaxRoot(depth, board, True, player)
        new_board = game.get_next_board(board, best, 's')
        player = game.reverse_player(player)
        board = new_board
        game.display(board)
    game.display(board)


if __name__ == '__main__':
    #print(is_over(classic_board))
    playGame(2)

