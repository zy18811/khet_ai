import numpy as np
from tqdm import tqdm
from ai.actions import convert_to_readable, is_terminal, possible_actions_4_state, apply_move, deepcopy, mirror_state, get_pos_4_coords
from ai.globals import *
import uuid
from multiprocessing import Pool, cpu_count
import sys

class Game:
    def __init__(self,evalulate_position = None):
        if evalulate_position is not None:
            self.evaluate_position = evalulate_position

    # TODO: better evaluation
    def evaluate_position(self,board,player):
        pos_score = 0
        # Positional evaluation
        for i in range(8):
            for j in range(10):
                piece = board[i][j]
                # Calculates value for each pyramid existing and its position
                if piece != 0:
                    if piece.type == 'pyr':
                        if piece.team == player:
                            pos_score -= piece.value
                        elif piece.team != player:
                            pos_score += piece.value
                        elif piece.team != player:
                            pos_score -= piece.value
                    # Calculates value for Obelisk's existing
                    elif piece.type == 'ob':
                        if piece.team == player:
                            pos_score += piece.value
                        elif piece.team != player:
                            pos_score -= piece.value
                    # Calculates value for Djed's positions
                    elif piece.type == 'dj':
                        pass
                    # Stores the location of the Pharoahs
                    elif piece.type == 'pha':
                        if piece.team == player:
                            pos_score += piece.value
                            player_pha_i = i
                            player_pha_j = j
                        elif piece.team != player:
                            pos_score -= piece.value
                            enemy_pha_i = i
                            enemy_pha_j = j
                    else:
                        pass
                else:
                    pass

        # Laser Manhattan Evaluation
        laser_shoot = lasershoot(board, player)
        manhattan_score = abs(laser_shoot[0]-enemy_pha_i + laser_shoot[1]-enemy_pha_j)
        pos_score -= manhattan_score / 4

        # King Safety Evaluation
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for direction in directions:
            try:
                piece = board(player_pha_i+direction[0], player_pha_j+direction[1])
                if piece != 0:
                    if piece.type == 'ob':
                        pos_score += piece.value
                    elif piece.type == 'sob':
                        pos_score += piece.value
                else:
                    pos_score -= 1
            except:
                pass

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


def update_visuals(move,board):
    move_locs = [int(e) for e in list(filter(str.isdigit, move))]
    x0 = move_locs[0]
    y0 = move_locs[1]
    piece = board[y0][x0]

    li = pyg.image.load

    facings = ['NE', 'SE', 'SW', 'NW']
    move = move[:-1]
    if move[0] == 'r':
        if move[-1] == 'L':
            new_facing = facings[(facings.index(piece.facing) - 1) % 4]
        elif move[-1] == 'R':
            new_facing = facings[(facings.index(piece.facing) + 1) % 4]
        if piece.type == 'pyr':
            classic_starting[(y0,x0)] = li(globals()[f'{piece.team}{piece.type}_{new_facing}'].image)
        elif piece.type == 'dj':
            if new_facing == 'NW' or new_facing == 'SE':
                classic_starting[(y0,x0)] = li(globals()[f'{piece.team}dj_NW_SE'].image)
            elif new_facing == 'NE' or new_facing == 'SW':

                classic_starting[(y0,x0)] = li(globals()[f'{piece.team}dj_NE_SW'].image)
    if move[0] == 'm':
        x1 = move_locs[2]
        y1 = move_locs[3]

        classic_starting[(y1,x1)] = li(piece.image)
        classic_starting[(y0,x0)] = None
    elif move[0] == 'd':
        x1 = move_locs[2]
        y1 = move_locs[3]

        classic_starting[(y0,x0)] = classic_starting[(y1,x1)]
        classic_starting[(y1,x1)] = li(piece.image)

    elif move[:2] == 'sp':
        x1 = move_locs[2]
        y1 = move_locs[3]

        classic_starting[(y0,x0)] = li(globals()[f'{piece.team}ob'].image)
        classic_starting[(y1,x1)] = li(globals()[f'{piece.team}ob'].image)

    elif move[:2] == 'st':
        x1 = move_locs[2]
        y1 = move_locs[2]

        classic_starting[(y0,x0)] = None
        classic_starting[(y1,x1)] = li(globals()[f'{piece.team}sob'].image)


def render_background(WIN):
    WIDTH = 1000
    HEIGHT = int((WIDTH / 10) * 8)
    bg = pyg.image.load(dir.joinpath("images/board.png"))
    bg = pyg.transform.smoothscale(bg, (WIDTH, HEIGHT))
    WIN.blit(bg, (0, 0))


def render_board(WIN):
    scale = 1000 / 1600
    piece_width = int(128 * scale) - 2
    piece_height = int(128 * scale) - 4

    render_background(WIN)
    for i in range(8):
        for j in range(10):
            if classic_starting[(i,j)] is not None:
                x = 115 * scale + 2 + j * (piece_width + 8.2)
                y = 110 * scale + 1 + i * (piece_height + 7.8)

                piece_img = classic_starting[(i,j)]

                piece_img = pyg.transform.smoothscale(piece_img.convert(), (piece_width, piece_height))
                WIN.blit(piece_img, (x, y))
    pyg.display.flip()


def laser_visual(board,player_colour):
    hit_target = False
    laser_start_tile = [(-1, 0), (8, 9)]
    laser_start_orientation = ["N", "S"]

    orients = ["N", "E", "S", "W"]
    orientation_val = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    pyramid_facings = ["NE", "SE", "SW", "NW"]
    pyramid_orientations = [("N", "E"), ("S", "E"), ("S", "W"), ("N", "W")]

    cur_tile = laser_start_tile[player_colour]
    cur_orientation = laser_start_orientation[player_colour]

    while not hit_target:
        try:
            next_tile = np.add(cur_tile, orientation_val[orients.index(cur_orientation)])
            x = next_tile[0]
            y = next_tile[1]
            if x < 0 or y < 0 or x > 7 or y > 9:
                if x == -1:
                    x = 0
                if y == -1:
                    y = 0
                if x == 8:
                    x = 7
                if y == 10:
                    y = 9

                if super_board[x][y] != 0:
                    super_super_board[x][y] = dir.joinpath("images/laser_splash_%s.png" % cur_orientation)
                else:
                    super_board[x][y] = dir.joinpath("images/laser_splash_%s.png" % cur_orientation)
                # other wall impact
                return

            # print(cur_orientation)
            if board[x][y] == 0:

                # Laser stuff for empty tile

                cur_tile = next_tile
                # print("empty")
                # Draw laser with current orientation
                if cur_orientation == 'N' or cur_orientation == "S":
                    if super_board[x][y] != 0:
                        super_super_board[x][y] = dir.joinpath("images/laser_NS.png")
                    else:
                        super_board[x][y] = dir.joinpath("images/laser_NS.png")
                else:
                    if super_board[x][y] != 0:
                        super_super_board[x][y] = dir.joinpath("images/laser_EW.png")
                    else:
                        super_board[x][y] = dir.joinpath("images/laser_EW.png")
                # Play sound
            elif board[x][y].type == "pyr":
                # Laser stuff for pyramids
                if cur_orientation in pyramid_orientations[pyramid_facings.index(board[x][y].facing)]:
                    # Change laser direction
                    ori_arr = [e for e in pyramid_orientations[pyramid_facings.index(board[x][y].facing)]]
                    ori_arr.remove(cur_orientation)

                    cur_orientation = orients[(orients.index(ori_arr[0]) + 2) % 4]
                    cur_tile = next_tile
                    # del_orients = numpy.concatenate(([cur_orientation] ,pyramid_orientations[pyramid_facings.index(board[x][y].facing)]))

                    # Draw laser bounce
                    if super_board[x][y] != 0:
                        super_super_board[x][y] = dir.joinpath("images/laser_%s.png" % board[x][y].facing)
                    else:
                        super_board[x][y] = dir.joinpath("images/laser_%s.png" % board[x][y].facing)

                    # Play sound
                else:
                    # Destroy piece
                    if super_board[x][y] != 0:
                        super_super_board[x][y] = dir.joinpath("images/laser_death_%s.png" % cur_orientation)
                    else:
                        super_board[x][y] = dir.joinpath("images/laser_death_%s.png" % cur_orientation)
                    classic_starting[(x,y)] = None
                    return


            elif board[x][y].type == "dj":

                # Laser stuff for Djeds
                # Change laser direction
                if cur_orientation in pyramid_orientations[pyramid_facings.index(board[x][y].facing)]:
                    ori_arr = [e for e in pyramid_orientations[pyramid_facings.index(board[x][y].facing)]]
                    ori_arr.remove(cur_orientation)
                    cur_orientation = orients[(orients.index(ori_arr[0]) + 2) % 4]
                    pic_facing = ''.join(pyramid_orientations[pyramid_facings.index(board[x][y].facing)])
                elif cur_orientation in pyramid_orientations[(pyramid_facings.index(board[x][y].facing) + 2) % 4]:
                    ori_arr = [e for e in pyramid_orientations[(pyramid_facings.index(board[x][y].facing) + 2) % 4]]
                    ori_arr.remove(cur_orientation)
                    cur_orientation = orients[(orients.index(ori_arr[0]) + 2) % 4]
                    pic_facing = ''.join(pyramid_orientations[(pyramid_facings.index(board[x][y].facing) + 2) % 4])
                cur_tile = next_tile

                # Draw bounce
                if super_board[x][y] != 0:
                    super_super_board[x][y] = dir.joinpath("images/laser_%s.png" % pic_facing)
                else:
                    super_board[x][y] = dir.joinpath("images/laser_%s.png" % pic_facing)
                # Play sound
            else:
                # Laser stuff for Pharoahs and Obelisks
                # Destroy piece
                super_board[x][y] = dir.joinpath("images/laser_death_%s.png" % cur_orientation)
                classic_starting[(x,y)] = None
                return
                # End laser function

        except Exception as e:
            # Draw the wall impact
            super_board[x][y] = dir.joinpath("laser_splash_%s.png" % cur_orientation)
            return


def clear_laser():
    global super_board, super_super_board
    super_board = np.zeros(shape=(8, 10), dtype=object)
    super_super_board = np.zeros(shape=(8, 10), dtype=object)


def render_laser(WIN,board,player):
    scale = 1000 / 1600
    piece_width = int(128 * scale) - 2
    piece_height = int(128 * scale) - 4

    for i in range(10):
        for j in range(8):
            try:
                img1 = pyg.image.load(super_board[j][i])
                img1 = pyg.transform.smoothscale(img1, (piece_width, piece_height))
                x,y = get_pos_4_coords(i,j)
                WIN.blit(img1,(x,y))
            except:
                pass
            try:
                img2 = pyg.image.load(super_super_board[j][i])
                img2 = pyg.transform.smoothscale(img2, (piece_width, piece_height))
                x, y = get_pos_4_coords(i, j)
                WIN.blit(img2, (x, y))
            except:
                pass

    pyg.display.flip()


def render_txt_game(txt_game):
    pyg.init()

    WIDTH = 1000
    HEIGHT = int((WIDTH / 10) * 8)
    WIN = pyg.display.set_mode((WIDTH, HEIGHT))

    pyg.display.set_caption("Khet")
    pyg.display.set_icon(pyg.image.load(ssob.image))

    render_background(WIN)
    render_board(WIN)
    pyg.display.flip()
    pyg.time.wait(2000)
    board = classic_board
    player = 's'

    while True:
        for event in pyg.event.get():
            if event == pyg.QUIT:
                pyg.quit()
                sys.exit()

        for move in open(txt_game,'r'):
            pyg.event.get()
            if move == 'DRAW' or move == 'WIN/LOSS':
                print(move)
            else:
                Game().display(board)
                update_visuals(move,board)
                render_board(WIN)
                pyg.time.wait(2000)

                board = Game().get_next_board(board,move[:-1],player)

                if player == 's':
                    player_num = 1
                else:
                    player_num = 0
                laser_visual(board,player_num)
                render_laser(WIN,board,player)
                pyg.time.wait(2000)

                clear_laser()
                render_laser(WIN,board,player)

                player = Game().reverse_player(player)
                pyg.event.pump()
                pyg.time.wait(2000)




if __name__ == '__main__':
    #playGame(2)
    render_txt_game('2264767c712c4678aa482728a7ef4641.txt')


