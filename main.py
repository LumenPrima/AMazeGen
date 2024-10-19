import argparse
import os
import importlib
import random
from maze import Maze
from utils import svg_to_png, save_svg, save_gcode

# Dynamically import all algorithm modules
algorithm_modules = {}
algorithm_dir = os.path.join(os.path.dirname(__file__), 'algorithms')
for filename in os.listdir(algorithm_dir):
    if filename.endswith('.py') and not filename.startswith('__'):
        module_name = filename[:-3]  # Remove .py extension
        module = importlib.import_module(f'algorithms.{module_name}')
        algorithm_modules[module_name] = module

# Function to generate short names
def generate_short_name(name):
    words = name.split('_')
    if len(words) > 1:
        return ''.join(word[0] for word in words)
    else:
        return name[:3]

# Dynamically create ALGO_MAP
ALGO_MAP = {generate_short_name(name): (name, getattr(module, f'generate_{name}', None)) 
            for name, module in algorithm_modules.items()}

# Create a reverse mapping from full names to short names
REVERSE_ALGO_MAP = {full_name: short_name for short_name, (full_name, _) in ALGO_MAP.items()}

# Debug: Print ALGO_MAP
print("ALGO_MAP contents:")
for short_name, (full_name, func) in ALGO_MAP.items():
    print(f"  {short_name}: ({full_name}, {'function' if func else 'None'})")

def generate_maze(width, height, algorithms, output_formats=None, num_mazes=5, generate_output=True, print_stats=False, image_path=None, output_dir='./output', seed=None, start_point=None, end_point=None, cell_size=10):
    if output_formats is None:
        output_formats = ['svg', 'png']
    
    if seed is not None:
        random.seed(seed)
    
    for algorithm_name, generate_func in algorithms:
        print(f"\nGenerating {num_mazes} mazes using {algorithm_name} algorithm:")
        difficulties = []
        unsolvable_count = 0
        
        for i in range(num_mazes):
            # Create a new maze instance with explicit cell_size
            maze = Maze(width, height, algorithm_name, generate_func, output_dir=output_dir, cell_size=cell_size)
            
            # Generate the maze
            if algorithm_name == 'maze_from_image':
                if image_path is None:
                    print("Error: Image path is required for maze_from_image algorithm.")
                    continue
                maze.generate()
            else:
                maze.generate()
            
            # Set custom start and end points if provided
            if start_point:
                maze.start = start_point
            if end_point:
                maze.finish = end_point
            
            # Calculate the difficulty of the maze
            difficulty = maze.calculate_difficulty()
            difficulties.append(difficulty)
            
            # Debug: Print start and finish points
            print(f"    Maze {i+1} - Start: {maze.start}, Finish: {maze.finish}")
            
            if generate_output:
                # Define output functions for different formats
                output_functions = {
                    'svg': lambda m, solved: save_svg(
                        m.to_svg_with_solution() if solved and m.find_path() else m.to_svg(),
                        os.path.join(output_dir, f'maze_{algorithm_name}_{i+1}_diff{difficulty:.2f}_{"solved" if solved else "unsolved"}.svg')
                    ),
                    'png': lambda m, solved: svg_to_png(
                        m.to_svg_with_solution() if solved and m.find_path() else m.to_svg(),
                        os.path.join(output_dir, f'maze_{algorithm_name}_{i+1}_diff{difficulty:.2f}_{"solved" if solved else "unsolved"}.png'),
                        width=800, height=800
                    ),
                    'gcode': lambda m, solved: save_gcode(
                        m.to_gcode(include_solution=solved and m.find_path()),
                        os.path.join(output_dir, f'maze_{algorithm_name}_{i+1}_diff{difficulty:.2f}_{"solved" if solved else "unsolved"}.gcode')
                    )
                }
                
                # Generate and save the maze in specified formats
                solution = maze.find_path()
                for format in output_formats:
                    if format not in output_functions:
                        print(f"Warning: Unsupported output format '{format}'. Skipping.")
                        continue
                    
                    # Generate unsolved maze
                    output_functions[format](maze, False)
                    print(f"    Maze saved in {format.upper()} format (unsolved version)")
                    
                    # Generate solved maze if a solution exists
                    if solution:
                        output_functions[format](maze, True)
                        print(f"    Maze saved in {format.upper()} format (solved version)")
                        print(f"    Solution found for maze {i+1}. Path length: {len(solution)}")
                    else:
                        print(f"    Warning: No solution found for maze {i+1}. Skipping solved version.")
                        unsolvable_count += 1
                
                print(f"    Difficulty: {difficulty:.2f}")
        
        # Print statistics only if print_stats is True
        if print_stats and difficulties:
            avg_difficulty = sum(difficulties) / len(difficulties)
            min_difficulty = min(difficulties)
            max_difficulty = max(difficulties)
            print(f"\nStatistics for {algorithm_name} algorithm:")
            print(f"    Average Difficulty: {avg_difficulty:.2f}")
            print(f"    Minimum Difficulty: {min_difficulty:.2f}")
            print(f"    Maximum Difficulty: {max_difficulty:.2f}")
            print(f"    Unsolvable Mazes: {unsolvable_count} out of {num_mazes}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate mazes with specified algorithms and output formats.")
    parser.add_argument("-x", "--width", type=int, default=10, help="Width of the maze (x-axis)")
    parser.add_argument("-y", "--height", type=int, default=10, help="Height of the maze (y-axis)")
    parser.add_argument("-a", "--algorithms", nargs='+', default=['pri'], 
                        choices=list(ALGO_MAP.keys()) + list(name for name, _ in ALGO_MAP.values()) + ['all'],
                        metavar="ALGO",
                        help="Algorithms to use for maze generation. Can use short names, full names, or 'all'. "
                             "Short names: " + ", ".join(ALGO_MAP.keys()) + ". "
                             "Full names: " + ", ".join(name for name, _ in ALGO_MAP.values()) + ". "
                             "Use 'all' to run all available algorithms.")
    parser.add_argument("-f", "--formats", nargs='+', default=['png'], 
                        choices=['svg', 'png', 'gcode'], help="Output formats for the maze")
    parser.add_argument("-n", "--num_mazes", type=int, default=1, help="Number of mazes to generate for each algorithm")
    parser.add_argument("--no_output", action="store_true", help="Do not generate output files, only calculate difficulties")
    parser.add_argument("--print_stats", action="store_true", help="Print statistics for each algorithm")
    parser.add_argument("--image_path", type=str, help="Path to the image file for maze_from_image algorithm")
    parser.add_argument("-o", "--output_dir", type=str, default='./output', help="Directory to save output files")
    parser.add_argument("--seed", type=int, help="Seed for random number generator")
    parser.add_argument("--start", type=int, nargs=2, metavar=('X', 'Y'), help="Start point coordinates (x y)")
    parser.add_argument("--end", type=int, nargs=2, metavar=('X', 'Y'), help="End point coordinates (x y)")
    parser.add_argument("--cell_size", type=int, default=10, help="Cell size in pixels for SVG and PNG output")
    
    args = parser.parse_args()
    
    # Handle 'all' option for algorithms
    if 'all' in args.algorithms:
        selected_algorithms = list(ALGO_MAP.values())
    else:
        # Convert short algorithm names to full names and get generate functions
        selected_algorithms = []
        for algo in args.algorithms:
            if algo in ALGO_MAP:
                selected_algorithms.append(ALGO_MAP[algo])
            elif algo in REVERSE_ALGO_MAP:
                selected_algorithms.append(ALGO_MAP[REVERSE_ALGO_MAP[algo]])
            else:
                print(f"Warning: Unknown algorithm '{algo}'. Skipping.")
    
    # Debug: Print selected algorithms
    print("\nSelected algorithms:")
    for algo in selected_algorithms:
        print(f"  {algo}")
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    generate_maze(args.width, args.height, selected_algorithms, args.formats, args.num_mazes, 
                  not args.no_output, args.print_stats, args.image_path, args.output_dir, 
                  args.seed, args.start, args.end, args.cell_size)
