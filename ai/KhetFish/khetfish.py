import uuid
from multiprocessing import Pool, cpu_count
import pickle
import numpy as np
from tqdm import tqdm

from ai.actions import convert_to_readable, is_terminal, possible_actions_4_state, apply_move, deepcopy, mirror_state, \
    laser_shoot, is_over
from ai.actions import convert_to_readable, is_terminal, possible_actions_4_state, apply_move, deepcopy, mirror_state, laser_shoot
import ai.evaluations as eval_funcs

class Game:
    def __init__(self,evalulate_position = None):
        self.board_caches = {}
        try:
            self.board_caches = pickle.load(open('board_caches.pkl','rb'))
        except:
            pass
        if evalulate_position is not None:
            self.evaluate_position = evalulate_position

    # TODO: better evaluation
    def evaluate_position(self, board, player):

        # Value of the pieces and location data is evaluated
        score = eval_funcs.piecevalue_evaluation(board, player)[0]
        location_data = eval_funcs.piecevalue_evaluation(board, player)[1]

        # Laser Manhattan Evaluation
        score -= eval_funcs.laser_depth(board, player, location_data)

        # Pharoah Defense Evaluation
        score += eval_funcs.pharoah_defense1(board, player, location_data)
        score += eval_funcs.pharoah_defense2(board, player, location_data)

        # 1-Threat Evaluation


        # n-Threat Evaluation

        #

        return score + np.random.normal(0,0.3)


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

    def isTerminal(self, board):
        return is_over(board)

    def reverse_player(self,player):
        if player == 's':
            return 'r'
        else:
            return 's'

    def mm(self,move, board,depth,isMaximizing,player):
        board = self.get_next_board(board, move,player)
        value = self.minimax(depth - 1, board, -np.inf, np.inf, not isMaximizing, player)
        self.board_caches[self.hash_board(board, depth-1, not isMaximizing, )] = value
        return [value, move]

    def mmWrapper(self,args):
        return self.mm(*args)

    def minimaxRoot(self, depth, board,isMaximizing,player):
        possibleMoves = self.valid_moves(board,player)

        d1_res = np.array([self.mm(move,board,1,isMaximizing,player) for move in possibleMoves])
        d1_moves = d1_res[:,1][d1_res[:,0].argsort()]
        """
        """
        perc = 0.33
        """
        """
        pos_moves = d1_moves[:int(perc*len(d1_moves))]

        args = [(move,board,depth,isMaximizing,player) for move in pos_moves]

        threads = cpu_count()
        with Pool(threads) as p:
            bestMoveList = np.array(list(tqdm(p.imap(self.mmWrapper, args), total=len(args))))
        return bestMoveList[:,1][np.argmax(bestMoveList[:,0])]

    def minimax(self,depth, board, alpha, beta, is_maximizing,player):

        if self.hash_board(board,depth,is_maximizing) in self.board_caches:
            return self.board_caches[self.hash_board(board, depth, is_maximizing)]

        if (depth == 0) or self.isTerminal(board):

            self.board_caches[self.hash_board(board, depth, is_maximizing)] = self.evaluate_position(board, player)
            return -self.evaluate_position(board,player)


        possibleMoves = self.valid_moves(board,player) if is_maximizing else self.valid_moves(board, self.reverse_player(player))

        if is_maximizing:
            bestMove = -np.inf
            for x in possibleMoves:
                move = x
                old_board = deepcopy(board)
                board = self.get_next_board(board,move,player)
                bestMove = max(bestMove, self.minimax(depth - 1, board, alpha, beta, not is_maximizing,player))
                self.board_caches[self.hash_board(board,depth-1,not is_maximizing)] = bestMove

                board = old_board
                alpha = max(alpha, bestMove)
                if beta <= alpha:
                    return bestMove
            return bestMove
        else:
            bestMove = np.inf
            player = self.reverse_player(player)
            for x in possibleMoves:
                move = x
                old_board = deepcopy(board)
                board = self.get_next_board(board,move,player)
                bestMove = min(bestMove, self.minimax(depth - 1, board, alpha, beta, not is_maximizing,player))
                self.board_caches[self.hash_board(board, depth-1, not is_maximizing)] = bestMove

                board = old_board
                beta = min(beta, bestMove)
                if (beta <= alpha):
                    return bestMove
            return bestMove

    def hash_board(self,board,depth, isMaximising):
        return convert_to_readable(board) + ' ' + str(depth) + ' ' + str(isMaximising)

    def display(self,board):
        print(convert_to_readable(board))


def playGame(depth):
    game = Game()
    board = classic_board

    player = 's'
    move_n = 1
    file_id = str(uuid.uuid4().hex)+f'_depth_{depth}'+'.txt'
    while not game.isTerminal(board):
        best = game.minimaxRoot(depth, board, True, player)
        new_board = game.get_next_board(board, best, player)

        player = game.reverse_player(player)
        board = new_board

        open(file_id,'a').write(best+'\n')
        if move_n == 100:
            pickle.dump(game.board_caches, open('board_caches.pkl','wb'),pickle.HIGHEST_PROTOCOL)
            open(file_id, 'a').write('DRAW')
            return
        move_n+=1

    pickle.dump(game.board_caches, open('board_caches.pkl', 'wb'), pickle.HIGHEST_PROTOCOL)
    if np.sum(np.isin([f'{p.team} {p.type}' for row in board for p in row if p != 0], ['s pha'])) == 0:
        open(file_id, 'a').write('RED WIN')
    elif np.sum(np.isin([f'{p.team} {p.type}' for row in board for p in row if p != 0], ['r pha'])) == 0:
        open(file_id,'a').write('SILVER WIN')

    return


if __name__ == '__main__':
    playGame(4)



