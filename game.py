import pygame as pyg
import sys


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
spha = Piece('s','pha','','silver_pharoah.png')
rpha = Piece('r','pha','','red_pharoah.png')


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

WIDTH = 1000
HEIGHT = int((WIDTH/10)*8)
WIN = pyg.display.set_mode((WIDTH, HEIGHT))



pyg.display.set_caption("Khet")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)


class Node:
    def __init__(self, row, col):
        scale = 1000/1600
        self.row = col
        self.col = row

        self.piece_width = int(128 * scale) - 2
        self.piece_height = int(128 * scale) - 4

        self.x = 115*scale+2 + row*(self.piece_width + 8.2)
        self.y = 110*scale+1 + col*(self.piece_height + 7.8)

        self.piece_width = int(128*scale)-1
        self.piece_height = int(128*scale)-4
        self.image = None
        self.occupied = 0


    def setup(self, WIN):
        if classic_starting[(self.row, self.col)]:
            if classic_starting[(self.row, self.col)] is None:
                self.image = None
            else:
                self.occupied = 1

                piece_img = classic_starting[(self.row, self.col)]



                piece_img = pyg.transform.smoothscale(piece_img, (self.piece_width,self.piece_height))
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

"""
def laser_shooter(player_colour, board):
    hit_target = False
    laser_start_tile = [(0,0), (7, 9)]
    laser_start_orientation = [(3), (1)]
    orientation_val = [-1, 1, 1, -1]
    cur_tile = laser_start_tile[player_colour]
    cur_orientation = laser_start_orientation[player_colour]
        while not hit_target:
            next_tile = [cur_tile[0] - orientation_val[cur_orientation], cur_tile[1] - orientation_val[cur_orientation]]
            if board[next_tile[0], next_tile[1]]==None:
                #Laser stuff for empty tile
            elif board[next_tile[0], next_tile[1]].type==pyr:
                #Laser stuff for pyramids
            elif board[next_tile[0], next_tile[1]].type==dj:
                #Laser stuff for djeds
            else:
                #Laser stuff for Pharoahs and Obelisks
"""


def update_display(win, grid):
    for row in grid:
        for spot in row:
            spot.setup(win)
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

def main(WIN, WIDTH):
    scale = 1000 / 1600
    piece_width = int(128 * scale) - 1
    piece_height = int(128 * scale) - 4

    grid = make_grid(8,10, WIDTH)

    dragged_piece = None
    drag_x = None
    drag_y = None

    while True:
        pyg.time.delay(50)  ##stops cpu dying
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
            if event.type == pyg.MOUSEBUTTONDOWN:
                pos = pyg.mouse.get_pos()
                drag_x,drag_y = pos
                x,y = find_node(pos,10,8)
                piece = get_piece_from_coords(classic_board,x,y)
                node = grid[y][x]
                dragged_piece = node
                clear_node(x, y)
            if event.type == pyg.MOUSEMOTION:
                if dragged_piece is not None:
                    drag_x,drag_y = pyg.mouse.get_pos()
            if event.type == pyg.MOUSEBUTTONUP:
                if dragged_piece is not None:
                    pos = pyg.mouse.get_pos()
                    x,y = find_node(pos,10,8)
                    set_board_image(x,y,dragged_piece.image)
                    dragged_piece = None


            refresh_display(WIN, grid)
            if dragged_piece is not None:
                if dragged_piece.image is not None:
                    WIN.blit(dragged_piece.image, (drag_x-piece_width/2, drag_y-piece_height/2))
                pyg.display.flip()
            else:
                pass



if __name__ == '__main__':
    main(WIN,WIDTH)

