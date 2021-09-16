import pygame as pyg
from PIL import Image
import sys


def rotate_90_r(image):
    img = Image.open(image)
    rotate_img = img.rotate(-90)
    rotate_img.save(image)

def rotate_90_l(image):
    img = Image.open(image)
    rotate_img = img.rotate(90)
    rotate_img.save(image)


class Piece:
    def __init__(self,team,piece_type,facing,image1,image2=None,image3 = None,image4 = None):
        self.team = team
        self.type = piece_type
        self.facing = facing
        self.image = image1


spyr = Piece('s','pyr','','silver_pyramid_NE.png')
rpyr = Piece('r','pyr','','red_pyramid_NE.png')
sdj = Piece('s','dj','','silver_jed_NE_SW.png')
rdj = Piece('r','dj','','red_jed_NE_SW.png')
sob = Piece('s','ob','','silver_obelisk_single.png')
rob = Piece('r','ob','','red_obelisk_single.png')
ssob = Piece('s','sob','','silver_obelisk_double.png')
rsob = Piece('r','sob','','red_obelisk_double.png')
spha = Piece('s','pha','','silver_pharoah.png')
rpha = Piece('r','pha','','red_pharoah.png')


classic_starting = {(0,0):None, (0,1):None, (0,2):None, (0,3):None, (0,4):pyg.image.load(rsob.image), (0,5):pyg.image.load(rpha.image),
                    (0,6):pyg.image.load(rsob.image), (0,7):pyg.image.load(rpyr.image), (0,8):None, (0,9):None,
                    (1,0):None,(1, 1):None, (1, 2):pyg.image.load(rpyr.image), (1, 3):None, (1,4):None, (1,5):None,
                    (1,6):None, (1,7):None, (1,8):None, (1,9):None, (2,0):None,(2,1):None, (2,2):None,
                    (2,3):pyg.image.load(spyr.image),(2,4):None,(2,5):None,(2,6):None,(2,7):None,(2,8):None,(2,9):None,
                    (3,0):pyg.image.load(rpyr.image),(3,1):None,(3,2):pyg.image.load(spyr.image), (3,3):None,
                    (3,4):pyg.image.load(rdj.image),(3,5):pyg.image.load(rdj.image),(3,6):None,
                    (3,7):pyg.image.load(rpyr.image),(3,8):None,(3,9):pyg.image.load(spyr.image),
                    (4, 0): pyg.image.load(rpyr.image), (4, 1): None, (4, 2): pyg.image.load(spyr.image), (4, 3): None,
                    (4, 4): pyg.image.load(sdj.image), (4, 5): pyg.image.load(sdj.image), (4, 6): None,
                    (4, 7): pyg.image.load(rpyr.image), (4, 8): None, (4, 9): pyg.image.load(spyr.image),
                    (5,0):None,(5,1):None,(5,2):None,(5,3):None,(5,4):None,(5,5):None,(5,6):pyg.image.load(rpyr.image),
                    (5,7):None,(5,8):None,(5,9):None,(6,0):None,(6,1):None,(6,2):None,(6,3):None,(6,4):None,(6,5):None,
                    (6,6):None, (6,7):pyg.image.load(spyr.image),(6,8):None,(6,9):None,(7,0):None, (7,1):None,
                    (7,2):pyg.image.load(spyr.image),(7,3):pyg.image.load(ssob.image),(7,4):pyg.image.load(spha.image),
                    (7,5):pyg.image.load(ssob.image),(7,6):None,(7,7):None,(7,8):None,(7,9):None}


WIDTH = 1000
HEIGHT = int((WIDTH/10)*8)
WIN = pyg.display.set_mode((WIDTH, HEIGHT))
bg = pyg.image.load("board.png")
bg = pyg.transform.scale(bg, (WIDTH, HEIGHT))
WIN.blit(bg,(0,0))


pyg.display.set_caption("Khet")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)


class Node:
    def __init__(self, row, col, width):
        self.row = col
        self.col = row
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.occupied = None

    def setup(self, WIN):
        if classic_starting[(self.row, self.col)]:
            if classic_starting[(self.row, self.col)] is None:
                pass
            else:
                piece_img = classic_starting[(self.row, self.col)]
                piece_img = pyg.transform.scale(piece_img, (int(128*(1000/1600)),int(128*(1000/1600))))
                WIN.blit(piece_img, (self.x, self.y))


def make_grid(rows,cols, width):
    grid = []
    gap = width // cols
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            node = Node(j, i, gap)
            grid[i].append(node)
            """
            if (i+j)%2 ==1:
                grid[i][j].colour = GREY
            """
    return grid


def update_display(win, grid, rows,cols, width):
    for row in grid:
        for spot in row:
            spot.setup(win)
    pyg.display.update()


def main(WIN, WIDTH):
    grid = make_grid(8,10, WIDTH)
    while True:
        pyg.time.delay(50)  ##stops cpu dying
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
            update_display(WIN, grid, 8,10, WIDTH)


if __name__ == '__main__':
    main(WIN,WIDTH)

