import pygame as pyg
pyg.init()
import numpy
import sys
import time


class Piece:
    def __init__(self,team,piece_type,facing,image):
        self.team = team
        self.type = piece_type
        self.facing = facing
        self.image = image


spyr_NE = Piece('s','pyr','NE','silver_pyramid_NE.png')
spyr_SE = Piece('s','pyr','SE','silver_pyramid_SE.png')
spyr_SW = Piece('s','pyr','SW','silver_pyramid_SW.png')
spyr_NW = Piece('s','pyr','NW','silver_pyramid_NW.png')

rpyr_NE = Piece('r','pyr','NE','red_pyramid_NE.png')
rpyr_SE = Piece('r','pyr','SE','red_pyramid_SE.png')
rpyr_SW = Piece('r','pyr','SW','red_pyramid_SW.png')
rpyr_NW = Piece('r','pyr','NW','red_pyramid_NW.png')

sdj_NE_SW = Piece('s','dj','NE','silver_jed_NE_SW.png')
sdj_NW_SE = Piece('s','dj','SE','silver_jed_NW_SE.png')

rdj_NE_SW = Piece('r','dj','NE','red_jed_NE_SW.png')
rdj_NW_SE = Piece('r','dj','SE','red_jed_NW_SE.png')

sob = Piece('s','ob','','silver_obelisk_single.png')
rob = Piece('r','ob','','red_obelisk_single.png')
ssob = Piece('s','sob','','silver_obelisk_double.png')
rsob = Piece('r','sob','','red_obelisk_double.png')
spha = Piece('s','pha','','silver_pharoah_new.png')
rpha = Piece('r','pha','','red_pharoah_new.png')


classic_starting = {(0,0):None, (0,1):None, (0,2):None, (0,3):None, (0,4):pyg.image.load(rsob.image), (0,5):pyg.image.load(rpha.image),
                    (0,6):pyg.image.load(rsob.image), (0,7):pyg.image.load(rpyr_SE.image), (0,8):None, (0,9):None,
                    (1,0):None,(1, 1):None, (1, 2):pyg.image.load(rpyr_SW.image), (1, 3):None, (1,4):None, (1,5):None,
                    (1,6):None, (1,7):None, (1,8):None, (1,9):None, (2,0):None,(2,1):None, (2,2):None,
                    (2,3):pyg.image.load(spyr_NW.image),(2,4):None,(2,5):None,(2,6):None,(2,7):None,(2,8):None,(2,9):None,
                    (3,0):pyg.image.load(rpyr_NE.image),(3,1):None,(3,2):pyg.image.load(spyr_SW.image), (3,3):None,
                    (3,4):pyg.image.load(rdj_NE_SW.image),(3,5):pyg.image.load(rdj_NW_SE.image),(3,6):None,
                    (3,7):pyg.image.load(rpyr_SE.image),(3,8):None,(3,9):pyg.image.load(spyr_NW.image),
                    (4, 0): pyg.image.load(rpyr_SE.image), (4, 1): None, (4, 2): pyg.image.load(spyr_NW.image), (4, 3): None,
                    (4, 4): pyg.image.load(sdj_NW_SE.image), (4, 5): pyg.image.load(sdj_NE_SW.image), (4, 6): None,
                    (4, 7): pyg.image.load(rpyr_NE.image), (4, 8): None, (4, 9): pyg.image.load(spyr_SW.image),
                    (5,0):None,(5,1):None,(5,2):None,(5,3):None,(5,4):None,(5,5):None,(5,6):pyg.image.load(rpyr_SE.image),
                    (5,7):None,(5,8):None,(5,9):None,(6,0):None,(6,1):None,(6,2):None,(6,3):None,(6,4):None,(6,5):None,
                    (6,6):None, (6,7):pyg.image.load(spyr_NE.image),(6,8):None,(6,9):None,(7,0):None, (7,1):None,
                    (7,2):pyg.image.load(spyr_NW.image),(7,3):pyg.image.load(ssob.image),(7,4):pyg.image.load(spha.image),
                    (7,5):pyg.image.load(ssob.image),(7,6):None,(7,7):None,(7,8):None,(7,9):None}


classic_board = [[0,0,0,0,rsob,rpha,rsob,rpyr_SE,0,0],
                 [0,0,rpyr_SW,0,0,0,0,0,0,0],
                 [0,0,0,spyr_NW,0,0,0,0,0,0],
                 [rpyr_NE,0,spyr_SW,0,rdj_NE_SW,rdj_NW_SE,0,rpyr_SE,0,spyr_NW],
                 [rpyr_SE,0,spyr_NW,0,sdj_NW_SE,sdj_NE_SW,0,rpyr_NE,0,spyr_SW],
                 [0,0,0,0,0,0,rpyr_SE,0,0,0],
                 [0,0,0,0,0,0,0,spyr_NE,0,0],
                 [0,0,spyr_NW,ssob,spha,ssob,0,0,0,0]]

super_board = [[0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0]]

super_super_board = [[0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0]]

WIDTH = 1000
HEIGHT = int((WIDTH/10)*8)
WIN = pyg.display.set_mode((WIDTH, HEIGHT))



pyg.display.set_caption("Khet")
pyg.display.set_icon(pyg.image.load("silver_obelisk_double.png"))
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

#Music
pyg.mixer.music.load('music.wav')
#pyg.mixer.music.play(-1)

class Node:
    def __init__(self, row, col,image =None):
        scale = 1000/1600
        self.row = col
        self.col = row

        self.piece_width = int(128 * scale) - 2
        self.piece_height = int(128 * scale) - 4

        self.x = 115*scale+2 + row*(self.piece_width + 8.2)
        self.y = 110*scale+1 + col*(self.piece_height + 7.8)

        self.piece_width = int(128*scale)-1
        self.piece_height = int(128*scale)-4
        self.image = image
        self.occupied = 0


    def setup(self, WIN):
        if classic_starting[(self.row, self.col)]:
            if classic_starting[(self.row, self.col)] is None:
                self.image = None
            else:
                self.occupied = 1

                piece_img = classic_starting[(self.row, self.col)]



                piece_img = pyg.transform.smoothscale(piece_img.convert(), (self.piece_width,self.piece_height))
                self.image = piece_img

                WIN.blit(piece_img, (self.x, self.y))


def make_grid(rows,cols, width):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            node = Node(j, i)
            grid[i].append(node)
            """
            if (i+j)%2 ==1:
                grid[i][j].colour = GREY
            """
    return grid


def laser_shooter(player_colour, board):
    hit_target = False
    laser_start_tile = [(0,0), (7, 9)]
    laser_start_orientation = ["N", "S"]

    x_s = laser_start_tile[player_colour][0]
    y_s = laser_start_tile[player_colour][1]

    super_board[x_s][y_s] = 'laser_NS.png'


    orients = ["N", "E", "S", "W"]
    orientation_val = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    pyramid_facings = ["NE", "SE", "SW", "NW"]
    pyramid_orientations = [("N", "E"), ("S", "E"), ("S", "W"), ("N", "W")]

    cur_tile = laser_start_tile[player_colour]
    cur_orientation = laser_start_orientation[player_colour]

    while not hit_target:
        try:
            next_tile = numpy.add(cur_tile, orientation_val[orients.index(cur_orientation)])

            x = next_tile[0]
            y = next_tile[1]


            if x<0 or y<0 or x > 7 or y > 9:
                # other wall impact

                hit_target = True
                return None, None
            #print(cur_orientation)
            if board[x][y] == 0:

                #Laser stuff for empty tile



                cur_tile = next_tile
                #print("empty")
                #Draw laser with current orientation
                if cur_orientation == 'N' or cur_orientation == "S":
                    if super_board[x][y] != 0:
                        super_super_board[x][y] = "laser_NS.png"
                    else:
                        super_board[x][y] = "laser_NS.png"
                else:
                    if super_board[x][y] != 0:
                        super_super_board[x][y] = "laser_EW.png"
                    else:
                        super_board[x][y] = "laser_EW.png"
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
                    if super_board[x][y] != 0:
                        super_super_board[x][y] = "laser_%s.png" % board[x][y].facing
                    else:
                        super_board[x][y] = "laser_%s.png" % board[x][y].facing
                    #Play sound
                else:
                    #Destroy piece
                    if super_board[x][y] != 0:
                        super_super_board[x][y] = "laser_death_%s.png" % cur_orientation
                    else:
                        super_board[x][y] = "laser_death_%s.png" % cur_orientation
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
                elif cur_orientation in pyramid_orientations[pyramid_facings.index(board[x][y].facing)+2]:
                    ori_arr = [e for e in pyramid_orientations[pyramid_facings.index(board[x][y].facing)]]
                    ori_arr.remove(cur_orientation)
                    cur_orientation = orients[(orients.index(ori_arr[0]) + 2) % 4]

                cur_tile = next_tile
                #Draw bounce
                if super_board[x][y] != 0:
                    super_super_board[x][y] = "laser_%s.png" % board[x][y].facing
                else:
                    super_board[x][y] = "laser_%s.png" % board[x][y].facing
                #Play sound
            else:
                #Laser stuff for Pharoahs and Obelisks
                #Destroy piece
                #board[x][y] = 0
                return y,x
                #End laser function


        except:
            #Draw the wall impact

            if super_board[x][y] != 0:
                super_super_board[x][y] = "laser_splash_%s.png" % cur_orientation
            else:
                super_board[x][y] = "laser_splash_%s.png" % cur_orientation
            hit_target = True
            return None, None

def destroy_piece(x, y, board):
    #Remove piece from board
    if board[x, y].type == "pha":
        pass
        # Play victory sound

        # Set screen to victory screen with restart button

    #Draw board again
    #Play sound
    #Set other player's turn




def update_display(win, grid):
    scale = 1000/1600
    piece_width = int(128 * scale)
    piece_height = int(128 * scale)
    for row in grid:
        for spot in row:
            spot.setup(win)
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

    pyg.display.update()


def find_node(pos,cols,rows):
    x = pos[0]
    y = pos[1]

    scale = 1000 / 1600
    start_x = 115*scale+2
    start_y = 110 * scale + 1
    piece_width = int(128 * scale) - 1
    piece_height = int(128 * scale) - 4
    for i in range(rows+1):
        for j in range(cols+1):
            end_x = 115*scale+2 + j*(piece_width + 8.2)
            end_y = 110*scale+1 + i*(piece_height + 7.8)
            if x > start_x and y > start_y:
                if x < end_x and y < end_y:
                    return (j-1,i-1)


def get_piece_from_coords(board,x,y):
    piece = board[y][x]
    return piece


def Do_Move(OriginalPos, FinalPosition, WIN):
    classic_starting[FinalPosition] = classic_starting[OriginalPos]
    classic_starting[OriginalPos] = None


def clear_node(x,y):
    classic_starting[(y,x)] = None


def get_pos_4_coords(x,y):
    scale = 1000 / 1600
    piece_width = int(128 * scale) - 1
    piece_height = int(128 * scale) - 4
    x_pos = 115 * scale + 2 + x * (piece_width + 8.2)
    y_pos = 110 * scale + 1 + y * (piece_height + 7.8)
    return x_pos,y_pos


def refresh_display(win, grid):
    bg = pyg.image.load("board.png")
    bg = pyg.transform.smoothscale(bg, (WIDTH, HEIGHT))
    WIN.blit(bg, (0, 0))
    update_display(win,grid)


def set_board_image(x,y,image):
    classic_starting[(y,x)] = image


def set_board(node,x,y,sob_special,p):
    if abs(node.row - y) >1  or abs(node.col - x) >1:
        return False
    if p == 's' and (x == 0 or (x == 8 and y == 0) or (x == 8 and y == 7)):
        return False
    if p == 'r' and (x == 9 or (x == 1 and y == 0) or (x == 1 and y == 7)):
        return False
    if classic_board[y][x] != 0 and (classic_board[y][x].type == 'pyr' or
        classic_board[y][x].type == 'sob' or
        classic_board[y][x].type == 'ob') and classic_board[node.row][node.col].type == 'dj':

        move_from = classic_board[node.row][node.col]
        move_to = classic_board[y][x]
        classic_board[node.row][node.col] = move_to
        classic_board[y][x] = move_from
        set_board_image(x,y,node.image)
        set_board_image(node.col,node.row,pyg.transform.smoothscale(pyg.image.load(move_to.image),
                                                            (node.piece_width, node.piece_height)))
        return True
    elif classic_board[y][x] == classic_board[node.row][node.col] and classic_board[y][x].type == 'ob':
        if classic_board[node.row][node.col].team == 's':
            classic_board[y][x] = ssob
            set_board_image(x,y ,pyg.transform.smoothscale(pyg.image.load('silver_obelisk_double.png'),
                                                           (node.piece_width, node.piece_height)))
        elif classic_board[node.row][node.col].team == 'r':
            classic_board[y][x] = rsob
            set_board_image(x, y, pyg.transform.smoothscale(pyg.image.load('red_obelisk_double.png'),
                                                            (node.piece_width, node.piece_height)))
        if node.row != y or node.col != x:
            classic_board[node.row][node.col] = 0
        return True
    elif classic_board[y][x] != 0:
        return False
    else:
        classic_board[y][x] = classic_board[node.row][node.col]
        set_board_image(x, y, node.image)
        if sob_special:
            return True
        elif node.row != y or node.col != x:
            classic_board[node.row][node.col] = 0
            return True

        else:
            return False


def rotate_piece(x,y,dir,current_p):
    piece = classic_board[y][x]
    if piece == 0:
        return False
    new_piece = None
    facings = ['NE', 'SE', 'SW', 'NW']
    if piece.type == 'ob' or piece.type == 'sob' or piece.type == 'pha':
        return False
    elif piece.type == 'pyr' or piece.type == 'dj':
        new_facing = facings[(facings.index(piece.facing)-dir)%4]
        if piece.team == 's':
            if piece.team == current_p:
                if piece.type == 'pyr':
                    new_piece = globals()[f'spyr_{new_facing}']
                if piece.type == 'dj':
                    if new_facing == 'SW' or new_facing == 'NE':
                        new_piece = globals()['sdj_NE_SW']
                    elif new_facing == 'SE' or new_facing == 'NW':
                        new_piece = globals()['sdj_NW_SE']
                classic_board[y][x] = new_piece
                classic_starting[(y, x)] = pyg.image.load(new_piece.image)
                return True
            else: return False

        if piece.team == 'r':
            if piece.team == current_p:
                if piece.type == 'pyr':
                    new_piece = globals()[f'rpyr_{new_facing}']
                if piece.type == 'dj':
                    if new_facing == 'SW' or new_facing == 'NE':
                        new_piece = globals()['rdj_NE_SW']
                    elif new_facing == 'SE' or new_facing == 'NW':
                        new_piece = globals()['rdj_NW_SE']

                classic_board[y][x] = new_piece
                classic_starting[(y,x)] = pyg.image.load(new_piece.image)
                return True
            else: return False


def sob_dragged_node(x,y,current_p):
    dn = Node(x,y)

    simg = pyg.image.load('silver_obelisk_single.png')
    rimg = pyg.image.load('red_obelisk_single.png')
    simg = pyg.transform.smoothscale(simg, (dn.piece_width, dn.piece_height))
    rimg = pyg.transform.smoothscale(rimg, (dn.piece_width, dn.piece_height))

    if current_p == 's' and classic_board[y][x].team == 's':
        dn.image = simg
        set_board_image(x,y,simg)
        classic_board[y][x] = sob
        return dn, make_grid(8,10,WIDTH)
    elif current_p == 'r' and classic_board[y][x].team == 'r':
        dn.image = rimg
        set_board_image(x,y,rimg)
        classic_board[y][x] = rob
        return dn , make_grid(8,10,WIDTH)


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


def alternate_players():
    while True:
        yield 's'
        yield 'r'

def set_super_boards_zero():
    global super_board
    for j in range(8):
        for i in range(10):
            super_board[j][i] = 0
            super_super_board[j][i] = 0


def main(WIN, WIDTH):

    clock = pyg.time.Clock()
    scale = 1000 / 1600
    piece_width = int(128 * scale) - 1
    piece_height = int(128 * scale) - 4

    grid = make_grid(8, 10, WIDTH)


    dragged_node = None
    drag_x = None
    drag_y = None
    select_x = None
    select_y = None

    sob_special = False

    move_made = False

    laser_fired = False
    hit_x = None
    hit_y = None

    alternate_p = alternate_players()
    current_p = next(alternate_p)
    while True:
        pyg.time.delay(50)  ##stops cpu dying
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
            if event.type == pyg.MOUSEBUTTONDOWN:
                if laser_fired:
                    set_super_boards_zero()
                    if hit_x is not None and hit_y is not None:
                        if classic_board[hit_y][hit_x].type == 'pyr' or classic_board[hit_y][hit_x].type == 'ob':
                            classic_board[hit_y][hit_x] = 0
                            clear_node(hit_x,hit_y)
                        elif classic_board[hit_y][hit_x].type == 'sob':
                            simg = pyg.image.load('silver_obelisk_single.png')
                            rimg = pyg.image.load('red_obelisk_single.png')
                            simg = pyg.transform.smoothscale(simg,(piece_width,piece_height))
                            rimg = pyg.transform.smoothscale(rimg,(piece_width,piece_height))
                            if classic_board[hit_y][hit_x].team == 'r':
                                classic_board[hit_y][hit_x] = rob
                                set_board_image(hit_x,hit_y,rimg)
                            elif classic_board[hit_y][hit_x].team == 's':
                                classic_board[hit_y][hit_x] = sob
                                set_board_image(hit_x,hit_y,simg)
                        elif classic_board[hit_y][hit_x].type == 'pha':
                            print(f"{classic_board[hit_y][hit_x].team} loses...")

                    laser_fired = False
                else:
                    pos = pyg.mouse.get_pos()
                    if move_made:
                        if current_p == 's':
                            if pos[0] > 880 and pos[1] > 765:
                                if pos[0] < 900 and pos[1] < 785:
                                    #print("silver lazer")
                                    hit_x, hit_y = laser_shooter(1,classic_board)

                                    laser_fired = True
                                    current_p = next(alternate_p)
                                    move_made = False

                        elif current_p == 'r':
                            if pos[0] > 100 and pos[1] > 20:
                                if pos[0] < 120 and pos[1] < 40:
                                    hit_x, hit_y = laser_shooter(0, classic_board)
                                    laser_fired = True
                                    current_p = next(alternate_p)
                                    move_made = False

                    else:
                        try:
                            x, y = find_node(pos, 10, 8)
                            select_x = x
                            select_y = y
                            if clock.tick()<500:
                                if event.button == 1:
                                    if rotate_piece(x,y,1,current_p):
                                        move_made = True
                                        #current_p = next(alternate_p)
                                    if classic_board[y][x] != 0 and classic_board[y][x].type == 'sob':
                                        try:dragged_node,grid = sob_dragged_node(x,y,current_p)
                                        except: pass
                                        sob_special = True
                                elif event.button == 3:
                                    if rotate_piece(x, y, -1, current_p):
                                        move_made = True
                                        #current_p = next(alternate_p)
                            else:
                                pos = pyg.mouse.get_pos()
                                drag_x,drag_y = pos

                                node = grid[y][x]

                                piece = classic_board[y][x]
                                if piece != 0 and piece.team == current_p:
                                    if dragged_node is None:
                                        dragged_node = node
                                        clear_node(x, y)
                        except TypeError:
                            pass
            if event.type == pyg.MOUSEMOTION:
                if dragged_node is not None:
                    drag_x,drag_y = pyg.mouse.get_pos()
            if event.type == pyg.MOUSEBUTTONUP:

                if dragged_node is not None:
                    pos = pyg.mouse.get_pos()
                    x,y = find_node(pos,10,8)
                    if set_board(dragged_node,x,y,sob_special,current_p) and (select_x != x or select_y != y):
                        move_made = True
                        #current_p = next(alternate_p)
                    else:
                        if sob_special:
                            pass
                        else:
                            set_board_image(select_x,select_y,dragged_node.image)
                    sob_special = False
                    dragged_node = None

                    #print(convert_to_readable(classic_board))

            refresh_display(WIN, grid)
            if dragged_node is not None:
                if dragged_node.image is not None:
                    WIN.blit(dragged_node.image, (drag_x-piece_width/2, drag_y-piece_height/2))
                    pyg.display.flip()



if __name__ == '__main__':
    main(WIN,WIDTH)

