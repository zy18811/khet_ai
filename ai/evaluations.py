
from ai.globals import *
from ai.actions import *
from numpy import *


def piecevalue_evaluation(board, player):
    location_data = []
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

    lasershoot_data = laser_shoot(board, player)
    manhattan_score = abs(lasershoot_data[0] - location_data[2] + lasershoot_data[1] - location_data[3])
    score = manhattan_score / 10

    return score


def pharoah_defense(board, player, location_data):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    score = 0
    for direction in directions:
        try:
            piece = board(location_data[0] + direction[0], location_data[1] + direction[1])
            if piece != 0:
                if piece.type == 'ob':
                    score += piece.value
                elif piece.type == 'sob':
                    score += piece.value
            else:
                score -= 1
        except:
            pass
    return score

