from PIL import Image

def generate_maze_from_image(maze, image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img = img.resize((maze.width * 2 + 1, maze.height * 2 + 1))
    grid = maze.grid

    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            grid[y][x] = 0 if pixel > 128 else 1  # Threshold at 128

    # Ensure start and finish are open
    grid[1][1] = 0
    grid[img.height - 2][img.width - 2] = 0
