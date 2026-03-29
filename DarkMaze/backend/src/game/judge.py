import numpy as np
import re
import json

def _parse_map(map_string, map_size, reversal_nodes=[]):
    width, height = map_size
    filtered_chars = re.sub(r'[^a-zA-Z]', '', map_string)

    binary_chars = [bin(ord(c))[2:].zfill(8) for c in filtered_chars]

    grid_values = []
    for bits in binary_chars:
        first_half = int(bits[:4], 2)
        second_half = int(bits[4:], 2)
        grid_values.extend([first_half % 2, second_half % 2])

    while len(grid_values) < width * height:
        grid_values.append(0)

    grid_values = grid_values[:width * height]

    grid = np.array(grid_values).reshape((height, width))

    for x, y in reversal_nodes:
        if 0 <= x < height and 0 <= y < width:
            grid[y, x] = 1 - grid[y, x]

    return grid

def _load_maze_from_json(maze_level_name):
    with open("./src/game/maze_level/" + maze_level_name + ".json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    maze_level_name = data.get("maze_level_name", "Unknown Level")
    map_size = tuple(data.get("map_size", [10, 10]))
    starting_position = tuple(data.get("starting_position", [0, 0]))
    end_position = tuple(data.get("end_position", [0, 0]))
    map_string = data.get("map", "")
    reversal_nodes = data.get("reversal_node", [])

    parsed_map = _parse_map(map_string, map_size, reversal_nodes)

    return {
        "maze_level_name": maze_level_name,
        "map_size": map_size,
        "starting_position": starting_position,
        "end_position": end_position,
        "map": parsed_map
    }

def hit_obstacle(position, maze_level_name):
    x, y = position
    maze_data = _load_maze_from_json(maze_level_name)
    grid = maze_data["map"]

    if 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]:
        return grid[y, x] == 1
    return True

def game_over(health):
    return health == 0 or health == 666

def arrive_at_destination(maze_level_name, current_position):
    with open("./src/game/maze_level/" + maze_level_name + ".json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    end_position = tuple(data.get("end_position", [0, 0]))
    return tuple(current_position) == end_position
