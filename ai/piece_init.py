import pathlib
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pyg
dir = pathlib.Path(__file__).parent.parent

class Piece:
    def __init__(self,team,piece_type,facing,value,image):
        self.team = team
        self.type = piece_type
        self.facing = facing
        self.value = value
        self.image = image


spyr_NE = Piece('s','pyr','NE',5,dir.joinpath('images/silver_pyramid_NE.png'))
spyr_SE = Piece('s','pyr','SE',5,dir.joinpath('images/silver_pyramid_SE.png'))
spyr_SW = Piece('s','pyr','SW',5,dir.joinpath('images/silver_pyramid_SW.png'))
spyr_NW = Piece('s','pyr','NW',5,dir.joinpath('images/silver_pyramid_NW.png'))

rpyr_NE = Piece('r','pyr','NE',5,dir.joinpath('images/red_pyramid_NE.png'))
rpyr_SE = Piece('r','pyr','SE',5,dir.joinpath('images/red_pyramid_SE.png'))
rpyr_SW = Piece('r','pyr','SW',5,dir.joinpath('images/red_pyramid_SW.png'))
rpyr_NW = Piece('r','pyr','NW',5,dir.joinpath('images/red_pyramid_NW.png'))

sdj_NE_SW = Piece('s','dj','NE',None,dir.joinpath('images/silver_jed_NE_SW.png'))
sdj_NW_SE = Piece('s','dj','SE',None,dir.joinpath('images/silver_jed_NW_SE.png'))

rdj_NE_SW = Piece('r','dj','NE',None,dir.joinpath('images/red_jed_NE_SW.png'))
rdj_NW_SE = Piece('r','dj','SE',None,dir.joinpath('images/red_jed_NW_SE.png'))

sob = Piece('s','ob','',1,dir.joinpath('images/silver_obelisk_single.png'))
rob = Piece('r','ob','',1,dir.joinpath('images/red_obelisk_single.png'))
ssob = Piece('s','sob','',2,dir.joinpath('images/silver_obelisk_double.png'))
rsob = Piece('r','sob','',2,dir.joinpath('images/red_obelisk_double.png'))
spha = Piece('s','pha','',10000,dir.joinpath('images/silver_pharoah_new.png'))
rpha = Piece('r','pha','',10000,dir.joinpath('images/red_pharoah_new.png'))


classic_board = [[0,0,0,0,rsob,rpha,rsob,rpyr_SE,0,0],
                 [0,0,rpyr_SW,0,0,0,0,0,0,0],
                 [0,0,0,spyr_NW,0,0,0,0,0,0],
                 [rpyr_NE,0,spyr_SW,0,rdj_NE_SW,rdj_NW_SE,0,rpyr_SE,0,spyr_NW],
                 [rpyr_SE,0,spyr_NW,0,sdj_NW_SE,sdj_NE_SW,0,rpyr_NE,0,spyr_SW],
                 [0,0,0,0,0,0,rpyr_SE,0,0,0],
                 [0,0,0,0,0,0,0,spyr_NE,0,0],
                 [0,0,spyr_NW,ssob,spha,ssob,0,0,0,0]]


def set_piece_values(vpyr,vob,vsob,vpha):
    global spyr_NE, spyr_SE, spyr_SW, spyr_NW, rpyr_NE, rpyr_SE, rdj_NE_SW, rpyr_NW, sob, rob, ssob, rsob, spha, rpha
    spyr_NE.value = vpyr
    spyr_SE.value = vpyr
    spyr_SW.value = vpyr
    spyr_NW.value = vpyr
    rpyr_NE.value = vpyr
    rpyr_SE.value = vpyr
    rpyr_SW.value = vpyr
    rpyr_NW.value = vpyr

    sob.value = vob
    rob = vob

    ssob= vsob
    rsob = vsob

    spha = vpha
    rpha = vpha

