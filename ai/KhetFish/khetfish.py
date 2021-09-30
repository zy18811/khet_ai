import uuid
from multiprocessing import Pool, cpu_count
import pickle
from tqdm import tqdm
from ai.actions import convert_to_readable, possible_actions_4_state, apply_move, deepcopy, mirror_state, is_over
import ai.evaluations as eval_funcs
from ai.globals import *


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
        score = 0
        # Value of the pieces and location data is evaluated
        score, location_data = eval_funcs.piecevalue_evaluation(board, player)

        # Laser Manhattan Evaluation
        score += eval_funcs.laser_depth(board, player, location_data)

        # Pharoah Defense Evaluation
        score += eval_funcs.pharoah_defense1(board, player, location_data)
        score += eval_funcs.pharoah_defense2(board, player, location_data)

        # 1-Threat Evaluation
        score += eval_funcs.threat1(board, player)

        # n-Threat Evaluation

        # Perulok evaluation
        score += eval_funcs.perulok_eval(board, player)

        return score + np.random.normal(0,0.25)

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

    def top_perc_pos_moves(self,board,player,perc):
        possibleMoves = self.valid_moves(board, player)
        move_and_ev = np.array([(move,self.evaluate_position(self.get_next_board(board,move,player),player)) for move in possibleMoves])
        return move_and_ev[move_and_ev[:,1].astype(float).argsort()[::-1]][:,0][:int(perc*len(move_and_ev))]

    def mm(self,depth,board,move,is_ai_silver,player):
        board = self.get_next_board(board,move,player)
        local_score = self.minimax(depth - 1, board, not is_ai_silver, -np.inf, np.inf, self.reverse_player(player))
        return local_score,move

    def mmWrapper(self,args):
        return self.mm(*args)

    def ai_move(self,depth,board,player):

        legal_moves = self.top_perc_pos_moves(board,player,0.33)
        args = [(depth,board,move,True,player) for move in legal_moves]

        threads = cpu_count()
        with Pool(threads) as p:
            bestMoveList = np.array(list(tqdm(p.imap(self.mmWrapper, args), total=len(args),desc = f'{player}',
                                              colour = 'WHITE' if player == 's' else 'RED')))

        pickle.dump(self.board_caches, open('board_caches.pkl', 'wb'), pickle.HIGHEST_PROTOCOL)

        #print(bestMoveList)

        return bestMoveList[:, 1][bestMoveList[:, 0].astype(float).argsort()][-1]



        #return bestMoveList[:, 1][bestMoveList[:, 0].astype(float).argsort()][-1]


    def minimax(self, depth,board, is_maxing_silver, alpha, beta,player):
        # if board in cache
        if self.hash_board(board,depth, is_maxing_silver) in self.board_caches:
            return self.board_caches[self.hash_board(board,depth, is_maxing_silver)]

        # if depth is 0 or game is over
        if depth == 0 or self.isTerminal(board):

            if self.isTerminal(board) and not is_maxing_silver:
                self.board_caches[self.hash_board(board, depth, is_maxing_silver)] = self.evaluate_position(board,
                                                                                                            self.reverse_player(player))
            else:
                self.board_caches[self.hash_board(board,depth, is_maxing_silver)] = self.evaluate_position(board,player)
            return self.board_caches[self.hash_board(board,depth, is_maxing_silver)]

        # else
        best_score = -np.inf if is_maxing_silver else np.inf
        
        for move in self.valid_moves(board,player):
            old_board = deepcopy(board)
            board = self.get_next_board(board,move,player)

            local_score = self.minimax(depth - 1,board, not is_maxing_silver, alpha,beta,self.reverse_player(player))
            self.board_caches[self.hash_board(board,depth - 1, not is_maxing_silver)] = local_score

            if is_maxing_silver:
                best_score = max(best_score, local_score)
                alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, local_score)
                beta = min(beta, best_score)

            board = old_board

            if beta <= alpha:
                break
                
        self.board_caches[self.hash_board(board,depth, is_maxing_silver)] = best_score
        return self.board_caches[self.hash_board(board,depth, is_maxing_silver)]

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
        best = game.ai_move(depth,board,player)
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
    #print(Game().evaluate_position(classic_board,'s'))
    playGame(2)




