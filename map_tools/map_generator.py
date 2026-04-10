import random

WIDTH = 200   # number of tiles horizontally
HEIGHT = 200  # number of tiles vertically

def generate_map(width, height):
    grid = []

    for y in range(height):
        row = []
        for x in range(width):
            r = random.random()

            if r < 0.7:
                tile = 0  # grass
            elif r < 0.9:
                tile = 1  # trees
            else:
                tile = 2  # water

            row.append(tile)
        grid.append(row)

    return grid


def smooth_map(grid, iterations=3):
    width = len(grid[0])
    height = len(grid)

    for _ in range(iterations):
        new_grid = []

        for y in range(height):
            new_row = []
            for x in range(width):
                counts = {0: 0, 1: 0, 2: 0}

                # check neighbors
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            counts[grid[ny][nx]] += 1

                # pick most common neighbor
                new_tile = max(counts, key=counts.get)
                new_row.append(new_tile)

            new_grid.append(new_row)

        grid = new_grid

    return grid


def save_map(grid, filename="map.txt"):
    with open(filename, "w") as f:
        for row in grid:
            f.write(" ".join(map(str, row)) + "\n")


# --- RUN ---
grid = generate_map(WIDTH, HEIGHT)
grid = smooth_map(grid, iterations=4)
save_map(grid)

print("Map generated!")