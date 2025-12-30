from rooms import *

def get_door_rect(layout, marker="."):
    coords = [
        (row_i, col_i)
        for row_i, row in enumerate(layout)
        for col_i, ch in enumerate(row)
        if ch == marker
    ]

    if not coords:
        return None
    
    rows = [r for r, _ in coords]
    cols = [c for _, c in coords]

    min_row = min(rows)
    max_row = max(rows)
    min_col = min(cols)
    max_col = max(cols)

    width = max_col - min_col + 1
    height = max_row - min_row + 1

    return (min_col, min_row, width, height)

print("ROOM_01 . :", get_door_rect(ROOM_01_MAP, "."))
print("ROOM_02 . :", get_door_rect(ROOM_02_MAP, "."))
print("ROOM_03 . :", get_door_rect(ROOM_03_MAP, "."))
print("ROOM_04 . :", get_door_rect(ROOM_04_MAP, "."))