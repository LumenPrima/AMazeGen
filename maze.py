import random
import os
from maze_utils import select_start_finish, calculate_difficulty
from maze_svg import to_svg, overlay_solution, to_svg_with_solution
from maze_gcode import to_gcode
from maze_pathfinding import find_path

class Maze:
    def __init__(self, width, height, algorithm, generate_func, output_dir='./output', cell_size=10):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width * 2 + 1)] for _ in range(height * 2 + 1)]
        self.start = None
        self.finish = None
        self.algorithm = algorithm
        self.generate_func = generate_func
        self.output_dir = output_dir
        self.cell_size = cell_size
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate(self):
        self.generate_func(self)
        select_start_finish(self)  # Call the imported function instead of a method

    def to_svg(self, margin=10):
        return to_svg(self, self.cell_size, margin)

    def overlay_solution(self, svg_content, margin=10):
        return overlay_solution(self, svg_content, self.cell_size, margin)

    def to_svg_with_solution(self, margin=10):
        return to_svg_with_solution(self, self.cell_size, margin)
    
    def to_gcode(self, margin=10, max_size=200, include_solution=False):
        return to_gcode(self, self.cell_size, margin, max_size, include_solution)

    def find_path(self):
        return find_path(self)

    def calculate_difficulty(self):
        return calculate_difficulty(self)
