ROOM_01_MAP = [
    "                                                .",
    "                                                .",
    "                                                .",
    "                                                .",
    "                                                .",
    "                                                .",
    "                                               gg",
    "                                             gggg",
    "                                           gggggg",
    "                                       gggggggggg",
    "                                  ggggggggggggggg",
    "                            ggggggggggggggggggggg",
    "                                         ggggggtt",
    "                    bb                      gggtt",
    "                                              gtt",
    "                                               tt",                
    "               bb                              tt",              
    "                                               tt",
    "                               bbb        g    tt",
    "                     bbb                 gggg  tt",
    "                                        gtttttttt",
    "                                         ggg   tt",
    "                                    bb         tt",
    "                                               tt",
    "                 g                             tt",
    "                ggg           bbb              tt",         
    "                 t     bbb                     tt",              
    "          bbb    t                             tt",             
    "                 t                             tt",                 
    "   P            ttt                            tt",                   
    "ggggggggggggggggggggggggggggggggggggggggggggggggg",

]

ROOM_02_MAP = [
    "#                                  #",
    "#                                  #",
    "#                                  #",
    "#                                  #",
    "                                   .",
    "                                   .",
    "                                   .",
    "                                   .",
    "                                   .",
    "####################################",

]


ROOM_03_MAP = [
    "#                                  #",
    "#                                  #",
    "#                                  #",
    "#                                  #",
    ".                                  #",
    ".               ###                #",
    ".                                  #",
    ".                                  #",
    ".                                  #",
    "####################################",

]

ROOMS = { 
    "room_01": {
        "layout": ROOM_01_MAP,
        "sky_top": (90, 160, 255),
        "sky_bottom": (180, 220, 255),
    },
    "room_02": {
       "layout": ROOM_02_MAP,
        "sky_top": (255, 140, 80),
        "sky_bottom": (120, 70, 160), 
    },
    "room_03": {
        "layout": ROOM_03_MAP,
        "sky_top": (10, 10, 40),
        "sky_bottom": (40, 40, 90),
    },
}

START_ROOM = "room_01"

DOORS = {
    "room_01": [
        {"id": "right_exit", 
        "rect": (49, 0, 1, 5), 
        "edge": "right", 
        "to": ("room_02", "left_exit")},
    ],
    "room_02": [
        {"id": "left_exit", 
        "rect": (-1, 4, 1, 5), 
        "edge": "left",
        "to": ("room_01", "right_exit")},

        {"id": "right_exit",  
        "rect": (36, 4, 1, 5), 
        "edge": "right",
        "to": ("room_03", "left_exit")},
    ],
    "room_03": [
        {"id": "left_exit", 
        "rect": (-1, 4, 1, 5), 
        "edge": "left",
        "to": ("room_02", "right_exit")},
    ],
}