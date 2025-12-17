from constants import *
from tiles import SolidTile
from hazards import SpikeTile, WaterTile

def build_level_from_ascii(layout, tile_size):
    solid_tiles = []
    hazard_tiles = []
    player_spawn = (0, 0)

    for row_index, row in enumerate(layout):
        for col_index, char in enumerate(row):
            x = col_index * tile_size
            y = row_index * tile_size

            if char == "#":
                solid_tiles.append(SolidTile(x, y, tile_size, tile_size, "brown"))
            elif char == "^":
                hazard_tiles.append(
                    SpikeTile(
                        x + (tile_size - SPIKE_SIZE) // 2,
                        y + tile_size - SPIKE_SIZE,
                        SPIKE_SIZE, 
                        SPIKE_SIZE, 
                        "up"
                    )
                )
            elif char == "v":
                hazard_tiles.append(
                    SpikeTile(
                        x + (tile_size - SPIKE_SIZE) // 2,
                        y, 
                        SPIKE_SIZE,
                        SPIKE_SIZE, 
                        "down"
                    )
                )
            elif char == "<":
                hazard_tiles.append(
                    SpikeTile(
                        x + tile_size - SPIKE_SIZE,
                        y + (tile_size - SPIKE_SIZE) // 2,
                        SPIKE_SIZE,
                        SPIKE_SIZE,
                        "left"
                    )
                )
            elif char == ">":
                hazard_tiles.append(
                    SpikeTile(
                        x,
                        y + (tile_size - SPIKE_SIZE) // 2, 
                        SPIKE_SIZE, 
                        SPIKE_SIZE, 
                        "right"
                    )
                )
            elif char == "~":
                water_height = int(tile_size * WATER_HEIGHT_RATIO)
                y_offset = tile_size - water_height
                hazard_tiles.append(WaterTile(x, y + y_offset, tile_size, water_height))
            elif char == "P":
                player_spawn = (x, y)
            elif char in (" ", "."):
                pass

    return solid_tiles, hazard_tiles, player_spawn