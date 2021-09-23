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


classic_board = [[0,0,0,0,rsob,rpha,rsob,rpyr_SE,0,0],
                 [0,0,rpyr_SW,0,0,0,0,0,0,0],
                 [0,0,0,spyr_NW,0,0,0,0,0,0],
                 [rpyr_NE,0,spyr_SW,0,rdj_NE_SW,rdj_NW_SE,0,rpyr_SE,0,spyr_NW],
                 [rpyr_SE,0,spyr_NW,0,sdj_NW_SE,sdj_NE_SW,0,rpyr_NE,0,spyr_SW],
                 [0,0,0,0,0,0,rpyr_SE,0,0,0],
                 [0,0,0,0,0,0,0,spyr_NE,0,0],
                 [0,0,spyr_NW,ssob,spha,ssob,0,0,0,0]]