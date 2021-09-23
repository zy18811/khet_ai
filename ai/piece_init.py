import numpy as np

class Piece:
    def __init__(self,team,piece_type,facing,value,image):
        self.team = team
        self.type = piece_type
        self.facing = facing
        self.value = value
        self.image = image


spyr_NE = Piece('s','pyr','NE',5,'silver_pyramid_NE.png')
spyr_SE = Piece('s','pyr','SE',5,'silver_pyramid_SE.png')
spyr_SW = Piece('s','pyr','SW',5,'silver_pyramid_SW.png')
spyr_NW = Piece('s','pyr','NW',5,'silver_pyramid_NW.png')

rpyr_NE = Piece('r','pyr','NE',5,'red_pyramid_NE.png')
rpyr_SE = Piece('r','pyr','SE',5,'red_pyramid_SE.png')
rpyr_SW = Piece('r','pyr','SW',5,'red_pyramid_SW.png')
rpyr_NW = Piece('r','pyr','NW',5,'red_pyramid_NW.png')

sdj_NE_SW = Piece('s','dj','NE',None,'silver_jed_NE_SW.png')
sdj_NW_SE = Piece('s','dj','SE',None,'silver_jed_NW_SE.png')

rdj_NE_SW = Piece('r','dj','NE',None,'red_jed_NE_SW.png')
rdj_NW_SE = Piece('r','dj','SE',None,'red_jed_NW_SE.png')

sob = Piece('s','ob','',1,'silver_obelisk_single.png')
rob = Piece('r','ob','',1,'red_obelisk_single.png')
ssob = Piece('s','sob','',2,'silver_obelisk_double.png')
rsob = Piece('r','sob','',2,'red_obelisk_double.png')
spha = Piece('s','pha','',1000,'silver_pharoah_new.png')
rpha = Piece('r','pha','',1000,'red_pharoah_new.png')


classic_board = [[0,0,0,0,rsob,rpha,rsob,rpyr_SE,0,0],
                 [0,0,rpyr_SW,0,0,0,0,0,0,0],
                 [0,0,0,spyr_NW,0,0,0,0,0,0],
                 [rpyr_NE,0,spyr_SW,0,rdj_NE_SW,rdj_NW_SE,0,rpyr_SE,0,spyr_NW],
                 [rpyr_SE,0,spyr_NW,0,sdj_NW_SE,sdj_NE_SW,0,rpyr_NE,0,spyr_SW],
                 [0,0,0,0,0,0,rpyr_SE,0,0,0],
                 [0,0,0,0,0,0,0,spyr_NE,0,0],
                 [0,0,spyr_NW,ssob,spha,ssob,0,0,0,0]]


def set_piece_values(vpyr,vob,vsob,vpha):
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

