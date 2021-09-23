from sklearn import preprocessing
#from game import convert_to_readable
from sklearn.preprocessing import OneHotEncoder
from piece_init import *
from copy import deepcopy
import numpy as np


def convert_to_readable(board):
    output = ''

    for i in board:
        for j in i:
            try:
                output += f"{j.team} {j.type} {j.facing}, "
            except:
                output += f"{j}, "
        output += '\n'
    return output


def get_flipped_piece(piece):
    if piece.team == 's':
        if piece.type == 'pyr':
            if piece.facing == 'NE':
                return rpyr_NE
            elif piece.facing == 'SE':
                return rpyr_SE
            elif piece.facing == 'SW':
                return rpyr_SW
            elif piece.facing  == 'NW':
                return rpyr_NW
        elif piece.type == 'dj':
            if piece.facing == 'NE':
                return rdj_NE_SW
            elif piece.facing == 'SE':
                return rdj_NW_SE
        elif piece.type == 'ob':
            return rob
        elif piece.type == 'sob':
            return rsob
        elif piece.type == 'pha':
            return rpha
    elif piece.team == 'r':
        if piece.type == 'pyr':
            if piece.facing == 'NE':
                return spyr_NE
            elif piece.facing == 'SE':
                return spyr_SE
            elif piece.facing == 'SW':
                return spyr_SW
            elif piece.facing  == 'NW':
                return spyr_NW
        elif piece.type == 'dj':
            if piece.facing == 'NE':
                return sdj_NE_SW
            elif piece.facing == 'SE':
                return sdj_NW_SE
        elif piece.type == 'ob':
            return sob
        elif piece.type == 'sob':
            return ssob
        elif piece.type == 'pha':
            return spha


def mirror_state(state):
    state = np.rot90(state, k = 2)
    for i in range(8):
        for j in range(10):
            if state[i][j] != 0:
                state[i][j] = get_flipped_piece(state[i][j])
    return state


def possible_actions_4_state(board):

    #r*x,y*L
    #r*x,y*R
    #m*x,y*x1,y1
    #split_sob*x,y*x1,y1
    #dj_swap*x,y*x1,y1
    #stack_ob*x,y*x1,y1
    player_colour = 's'
    actions = []
    for j in range(8):
        for i in range(10):
            piece = board[j][i]
            if piece != 0 and piece.team == player_colour:
                #print(i,j)
                for m in range(j-1,j+2):
                    for n in range(i-1,i+2):
                        if (0 <= m <= 7) and (0 <= n <= 9) and not ( m==j and n == i):
                            if board[m][n] == 0:
                                if n != 0 or (n != 8 and m != 0) or (n != 8 and m != 7):
                                    actions.append(f'm*{i},{j}*{n},{m}')
                                    if piece.type == 'sob':
                                        actions.append(f'split_sob*{i},{j}*{n},{m}')
                            elif piece.type == 'ob' and board[m][n].type == 'ob' and board[m][n].team == player_colour:
                                actions.append(f'stack_ob*{i},{j}*{n},{m}')
                            elif piece.type == 'dj' and (board[m][n].type =='pyr' or board[m][n].type == 'ob' or board[m][n].type == 'sob'):
                                actions.append(f'dj_swap*{i},{j}*{n},{m}')
                if piece.type == 'pyr' or piece.type == 'dj':
                    actions.append(f'r*{i},{j}*L')
                    actions.append(f'r*{i},{j}*R')
    return actions


def all_actions():
    all_acts = []
    for j in range(8):
        for i in range(10):
            all_acts.append(f'r*{i},{j}*L')
            all_acts.append(f'r*{i},{j}*R')
            for m in range(j - 1, j + 2):
                for n in range(i - 1, i + 2):
                    if (0 <= m <= 7) and (0 <= n <= 9) and not (m == j and n == i):
                        all_acts.append(f'm*{i},{j}*{n},{m}')
                        all_acts.append(f'split_sob*{i},{j}*{n},{m}')
                        all_acts.append(f'stack_ob*{i},{j}*{n},{m}')
                        all_acts.append(f'dj_swap*{i},{j}*{n},{m}')

    return all_acts


def laser_shoot(board):
    hit_target = False
    laser_start_tile = [(-1, 0), (8, 9)]
    laser_start_orientation = ["N", "S"]

    orients = ["N", "E", "S", "W"]
    orientation_val = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    pyramid_facings = ["NE", "SE", "SW", "NW"]
    pyramid_orientations = [("N", "E"), ("S", "E"), ("S", "W"), ("N", "W")]

    cur_tile = laser_start_tile[0]
    cur_orientation = laser_start_orientation[0]

    while not hit_target:
        try:
            next_tile = np.add(cur_tile, orientation_val[orients.index(cur_orientation)])

            x = next_tile[0]
            y = next_tile[1]

            if x<0 or y<0 or x > 7 or y > 9:
                if x == -1:
                    x = 0
                if y == -1:
                    y = 0
                if x == 8:
                    x = 7
                if y == 10:
                    y = 9

                hit_target = True
                return None, None
            #print(cur_orientation)
            if board[x][y] == 0:

               #Laser stuff for empty tile

                cur_tile = next_tile
                #print("empty")
                #Draw laser with current orientation
                #Play sound
            elif board[x][y].type == "pyr":

                #Laser stuff for pyramids
                if cur_orientation in pyramid_orientations[pyramid_facings.index(board[x][y].facing)]:
                    #Change laser direction
                    ori_arr = [e for e in pyramid_orientations[pyramid_facings.index(board[x][y].facing)]]
                    ori_arr.remove(cur_orientation)

                    cur_orientation = orients[(orients.index(ori_arr[0]) + 2) % 4]
                    cur_tile = next_tile
                    #del_orients = numpy.concatenate(([cur_orientation] ,pyramid_orientations[pyramid_facings.index(board[x][y].facing)]))

                    #Draw laser bounce
                    #Play sound
                else:
                    #Destroy piece

                    #End laser function
                    hit_target = True
                    return y, x

            elif board[x][y].type == "dj":

                #Laser stuff for Djeds
                #Change laser direction
                if cur_orientation in pyramid_orientations[pyramid_facings.index(board[x][y].facing)]:
                    ori_arr = [e for e in pyramid_orientations[pyramid_facings.index(board[x][y].facing)]]
                    ori_arr.remove(cur_orientation)
                    cur_orientation = orients[(orients.index(ori_arr[0]) + 2) % 4]
                elif cur_orientation in pyramid_orientations[(pyramid_facings.index(board[x][y].facing)+2)%4]:
                    ori_arr = [e for e in pyramid_orientations[(pyramid_facings.index(board[x][y].facing)+2)%4]]
                    ori_arr.remove(cur_orientation)
                    cur_orientation = orients[(orients.index(ori_arr[0]) + 2) % 4]
                cur_tile = next_tile


            else:
                #Laser stuff for Pharoahs and Obelisks
                #Destroy piece

                return y,x
                #End laser function


        except Exception as e:
            hit_target = True
            return None, None


def laser_eval(state):
    hit_x, hit_y = laser_shoot(state)
    if hit_x is not None and hit_y is not None:
        hit_piece = state[hit_y][hit_x]
        state[hit_y][hit_x] = 0
    else:
        hit_piece = None
    return state, hit_piece


def is_terminal(state):
    state, hit_piece = laser_eval(state)
    if hit_piece is not None and hit_piece.type == 'pha':
        return True
    else: return False


def apply_move(move, state):
    n_state = deepcopy(state)
    facings = ['NE','SE','SW','NW']
    move_locs = [int(e) for e in list(filter(str.isdigit,move))]
    x0 = move_locs[0]
    y0 = move_locs[1]
    piece = n_state[y0][x0]

    #print(move)
    #print(possible_actions_4_state(state))
    #print(convert_to_readable(state))
    if move[0] == 'r':
        if move[-1] == 'L':
            new_facing = facings[(facings.index(piece.facing) - 1) % 4]
        elif move[-1] == 'R':
            new_facing = facings[(facings.index(piece.facing) + 1) % 4]
        if piece.type == 'pyr':
            n_state[y0][x0] = globals()[f's{piece.type}_{new_facing}']
        elif piece.type == 'dj':
            if new_facing == 'NW' or new_facing == 'SE':
                n_state[y0][x0] = sdj_NW_SE
            elif new_facing == 'NE' or new_facing == 'SW':
                n_state[y0][x0] = sdj_NE_SW
    if move[0] == 'm':
        x1= move_locs[2]
        y1 = move_locs[3]
        n_state[y1][x1] = piece
        n_state[y0][x0] = 0
    elif move[0] == 'd':
        x1 = move_locs[2]
        y1 = move_locs[3]
        n_state[y0][x0] = n_state[y1][x1]
        n_state[y1][x1] = piece

    elif move[:2] == 'sp':
        x1 = move_locs[2]
        y1 = move_locs[3]
        n_state[y0][x0] = sob
        n_state[y1][x1] = sob

    elif move[:2] == 'st':
        x1 = move_locs[2]
        y1 = move_locs[2]
        n_state[y0][x0] = 0
        n_state[y1][x1] = ssob

    n_state,_ = laser_eval(n_state)
    return n_state




if __name__ == '__main__':
    print(len(all_actions()))





                