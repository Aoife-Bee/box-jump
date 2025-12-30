from constants import *
from solid_tiles import SolidTile
from hazards import SpikeTile
from liquid_tiles import WaterTile, SwampWaterTile
from collectables import GoalOrb

def build_level_from_ascii(layout, tile_size):
    solid_tiles = []
    hazard_tiles = []
    liquid_tiles = []
    player_spawn = (0, 0)
    goal = None

    for row_index, row in enumerate(layout):
        for col_index, char in enumerate(row):
            x = col_index * tile_size
            y = row_index * tile_size

            if char == "g": #grass
                solid_tiles.append(SolidTile(x, y, tile_size, tile_size, (94, 182, 30)))
            elif char == "c": #cloud
                solid_tiles.append(SolidTile(x, y, tile_size, tile_size, ("beige")))
            elif char == "#": #rock
                 solid_tiles.append(SolidTile(x, y, tile_size, tile_size, (75, 93, 61)))
            elif char == "s": #slime tile
                 solid_tiles.append(SolidTile(x, y, tile_size, tile_size, (61, 63, 6)))
            elif char == "t": #tree
                 solid_tiles.append(SolidTile(x, y, tile_size, tile_size, (150, 75, 0)))
            elif char == "b": #bone
                 solid_tiles.append(SolidTile(x, y, tile_size, tile_size, (100, 100, 100)))

                 
            elif char == "^":
                    spike_u = SpikeTile(
                        x + (tile_size - SPIKE_SIZE) // 2,
                        y + tile_size - SPIKE_SIZE,
                        SPIKE_SIZE, 
                        SPIKE_SIZE, 
                        "up"
                    )
                    hazard_tiles.append(spike_u)
                    solid_tiles.append(spike_u)
            elif char == "v":
                    spike_d = SpikeTile(
                        x + (tile_size - SPIKE_SIZE) // 2,
                        y, 
                        SPIKE_SIZE,
                        SPIKE_SIZE, 
                        "down"
                    )
                    hazard_tiles.append(spike_d)
                    solid_tiles.append(spike_d)
            elif char == "<":
                    spike_l = SpikeTile(
                        x + tile_size - SPIKE_SIZE,
                        y + (tile_size - SPIKE_SIZE) // 2,
                        SPIKE_SIZE,
                        SPIKE_SIZE,
                        "left"
                    )
                    hazard_tiles.append(spike_l)
                    solid_tiles.append(spike_l)
            elif char == ">":
                spike_r = SpikeTile(
                        x,
                        y + (tile_size - SPIKE_SIZE) // 2, 
                        SPIKE_SIZE, 
                        SPIKE_SIZE, 
                        "right"
                    )
                hazard_tiles.append(spike_r)
                solid_tiles.append(spike_r)

            elif char == "~":
                liquid_tiles.append(SwampWaterTile(x, y, tile_size, tile_size, (128, 128, 0), depth=1.0))
            elif char == "=":
                liquid_tiles.append(SwampWaterTile(x, y, tile_size, tile_size, (138, 138, 0), depth=0.6))

            elif char == "P":
                player_spawn = (x, y)

            elif char == "*":
                 goal = GoalOrb(
                      x + tile_size // 2,
                      y + tile_size // 2,
                      radius=14
                 )
                 

            elif char in (" ", "."):
                pass

    return solid_tiles, hazard_tiles, liquid_tiles, player_spawn, goal