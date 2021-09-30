
from ai.globals import *
from ai.actions import *
from numpy import *


def piecevalue_evaluation(board, player):
    location_data = [0]*4
    score = 0
    for i in range(8):
        for j in range(10):
            piece = board[i][j]

            # Calculates value for each pyramid existing and its position
            if piece != 0:
                if piece.type == 'pyr':
                    if piece.team == player:
                        score += piece.value
                    elif piece.team != player:
                        score -= piece.value

                # Calculates value for Obelisk's existing
                elif piece.type == 'ob' or piece.type == 'sob':
                    if piece.team == player:
                        score += piece.value
                    elif piece.team != player:
                        score -= piece.value
                # Calculates value for Djed's positions
                elif piece.type == 'dj':
                    pass
                # Stores the location of the Pharoahs
                elif piece.type == 'pha':
                    if piece.team == player:
                        score += piece.value
                        location_data[0] = i
                        location_data[1] = j
                    elif piece.team != player:
                        score -= piece.value
                        location_data[2] = i
                        location_data[3] = j
                else:
                    pass
            else:
                pass

    return score, location_data


def laser_depth(board, player, location_data):
    score = 0
    lasershoot_data = laser_shoot(board, player)
    manhattan_score = abs(lasershoot_data[0] - location_data[2] + lasershoot_data[1] - location_data[3])
    score -= manhattan_score / 10

    return score


def pharoah_defense1(board, player, location_data):
    # Checking the Pharoah defense with depth 1
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    score = 0
    for direction in directions:
        try:
            piece = board(location_data[0] + direction[0], location_data[1] + direction[1])
            if piece != 0:
                if piece.team == player:
                    score += piece.value
                elif piece.type == 'dj':
                    score -= 1
                else:
                    score -= piece.value
            else:
                score -= 1
        except:
            pass

    return score


def pharoah_defense2(board, player, location_data):
    # Doing a double orthogonal calculation
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    score = 0
    for first_direction in directions:
        for second_direction in directions:
            try:
                piece = board(location_data[0] + first_direction[0] + second_direction[0], location_data[1]+first_direction[1]+second_direction[1])
                if piece != 0 and piece.type != 'pha':
                    if piece.team == player:
                        score += piece.value * 0.5
                    else:
                        score -= piece.value * 0.5
                else:
                    pass
            except:
                pass

    return score


def threat1(board, player):
    # Evaluating one move threats
    score = 0
    coords = laser_shoot(board, player)
    if coords[2]:
        if board[coords[1]][coords[0]].team == player:
            score -= 1
        else:
            score += 1

    return score


def perulok_eval(board, player):
    score = 0
    counter = 0
    s_rows = [8, 9]
    r_rows = [0, 1]
    columns = range(0, 7)

    while counter <= 3:
        if player == 's':
            for x in s_rows:
                for y in columns:
                    z = board[x][y]
                    if z != 0 and z.team == 's' and ((z.type == 'pyr' and z.facing == 'SW') or (z.type == 'dj' and z.facing == 'NE')):
                        score += 1
                        counter +=1
        else:
            for x in r_rows:
                for y in columns:
                    z = board[x][y]
                    if z != 0 and z.team == 'r' and ((z.type == 'pyr' and z.facing == 'NE') or (z.type == 'dj' and z.facing == 'NE')):
                        score += 1
                        counter += 1

    return score

