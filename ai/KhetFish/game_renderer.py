from ai.globals import *
from ai.actions import get_pos_4_coords
from khetfish import Game,sys


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
                if board[x][y].type == 'sob':
                    if player_colour == 1:
                        classic_starting[(x,y)] = sob.image
                    elif player_colour ==0:
                        classic_starting[(x,y)] = rob.image
                else:
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
                #Game().display(board)
                update_visuals(move,board)
                render_board(WIN)
                pyg.time.wait(1000)
                #Game().display(board)
                board = Game().get_next_board(board,move[:-1],player)

                if player == 's':
                    player_num = 1
                else:
                    player_num = 0

                laser_visual(board,player_num)
                render_laser(WIN,board,player)
                pyg.time.wait(1000)

                clear_laser()
                render_laser(WIN,board,player)

                player = Game().reverse_player(player)
                pyg.event.pump()
                pyg.time.wait(1000)

if __name__ == '__main__':
    render_txt_game('')