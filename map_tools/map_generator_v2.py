import random

WIDTH = 300
HEIGHT = 300

def generate_map(width, height):
    grid = []

    for y in range(height):
        row = []
        for x in range(width):

            # layered randomness (fake "biomes")
            r = random.random()
            edge_bias = min(x/width, y/height, (width-x)/width, (height-y)/height)

            if r < 0.55:
                tile = 0  # grass
            elif r < 0.7:
                tile = 1  # forest
            elif r < 0.8:
                tile = 3  # sand
            elif r < 0.9:
                tile = 2  # water
            elif r < 0.97:
                tile = 4  # mountain
            else:
                tile = 5  # lava

            # more water near edges (like oceans)
            if edge_bias < 0.1 and random.random() < 0.6:
                tile = 2

            row.append(tile)

        grid.append(row)

    return grid


def smooth_map(grid, iterations=3):
    width = len(grid[0])
    height = len(grid)

    for _ in range(iterations):
        new = []

        for y in range(height):
            row = []
            for x in range(width):
                counts = {}

                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < width and 0 <= ny < height:
                            tile = grid[ny][nx]
                            counts[tile] = counts.get(tile, 0) + 1

                row.append(max(counts, key=counts.get))
            new.append(row)

        grid = new

    return grid


def save_map(grid, filename="map.txt"):
    with open(filename, "w") as f:
        for row in grid:
            f.write(" ".join(map(str, row)) + "\n")


grid = generate_map(WIDTH, HEIGHT)
grid = smooth_map(grid, 4)
save_map(grid)

print("Better map generated!")