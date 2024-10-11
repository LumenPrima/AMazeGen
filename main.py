import argparse
from maze import Maze
from maze_algorithms import (
    generate_dfs, generate_kruskal, generate_prim, generate_recursive_division,
    generate_aldous_broder, generate_wilsons, generate_hunt_and_kill,
    generate_ellers, generate_sidewinder, generate_binary_tree,
    generate_growing_tree, generate_recursive_backtracker, generate_cellular_automata,
    generate_kruskal_weighted, generate_aldous_broder_optimized
)
from utils import svg_to_png, save_svg, save_gcode

# Mapping of short names to full algorithm names
ALGO_MAP = {
    'dfs': 'dfs',
    'kru': 'kruskal',
    'pri': 'prim',
    'rd': 'recursive_division',
    'ab': 'aldous_broder',
    'wil': 'wilsons',
    'hk': 'hunt_and_kill',
    'ell': 'ellers',
    'sw': 'sidewinder',
    'bt': 'binary_tree',
    'gt': 'growing_tree',
    'rb': 'recursive_backtracker',
    'ca': 'cellular_automata',
    'kw': 'kruskal_weighted',
    'abo': 'aldous_broder_optimized'
}

def generate_maze(width, height, algorithms, output_formats=None, num_mazes=5, generate_output=True, print_stats=False):
    if output_formats is None:
        output_formats = ['svg', 'png']
    
    for algorithm in algorithms:
        print(f"\nGenerating {num_mazes} mazes using {algorithm} algorithm:")
        difficulties = []
        
        for i in range(num_mazes):
            # Create a new maze instance
            maze = Maze(width, height, algorithm)
            
            # Generate the maze using the specified algorithm
            if algorithm == 'dfs':
                generate_dfs(maze)
            elif algorithm == 'kruskal':
                generate_kruskal(maze)
            elif algorithm == 'prim':
                generate_prim(maze)
            elif algorithm == 'recursive_division':
                generate_recursive_division(maze)
            elif algorithm == 'aldous_broder':
                generate_aldous_broder(maze)
            elif algorithm == 'wilsons':
                generate_wilsons(maze)
            elif algorithm == 'hunt_and_kill':
                generate_hunt_and_kill(maze)
            elif algorithm == 'ellers':
                generate_ellers(maze)
            elif algorithm == 'sidewinder':
                generate_sidewinder(maze)
            elif algorithm == 'binary_tree':
                generate_binary_tree(maze)
            elif algorithm == 'growing_tree':
                generate_growing_tree(maze, selection_method='random')
            elif algorithm == 'recursive_backtracker':
                generate_recursive_backtracker(maze)
            elif algorithm == 'cellular_automata':
                generate_cellular_automata(maze)
            elif algorithm == 'kruskal_weighted':
                generate_kruskal_weighted(maze)
            elif algorithm == 'aldous_broder_optimized':
                generate_aldous_broder_optimized(maze)
            else:
                raise ValueError(f"Unknown algorithm: {algorithm}")
            
            # Select start and finish points
            maze.select_start_finish()

            # Calculate the difficulty of the maze
            difficulty = maze.calculate_difficulty()
            difficulties.append(difficulty)
            
            if generate_output:
                # Define output functions for different formats
                output_functions = {
                    'svg': lambda m, solved: save_svg(
                        m.to_svg_with_solution() if solved else m.to_svg(),
                        f'maze_{algorithm}_{i+1}_{"solved" if solved else "unsolved"}.svg'
                    ),
                    'png': lambda m, solved: svg_to_png(
                        m.to_svg_with_solution() if solved else m.to_svg(),
                        f'maze_{algorithm}_{i+1}_{"solved" if solved else "unsolved"}.png',
                        width=800, height=800
                    ),
                    'gcode': lambda m, solved: save_gcode(
                        m.to_gcode(include_solution=solved),
                        f'maze_{algorithm}_{i+1}_{"solved" if solved else "unsolved"}.gcode'
                    )
                }
                
                # Generate and save the maze in specified formats
                for format in output_formats:
                    if format not in output_functions:
                        print(f"Warning: Unsupported output format '{format}'. Skipping.")
                        continue
                    
                    # Generate unsolved maze
                    output_functions[format](maze, False)
                    
                    # Generate solved maze
                    output_functions[format](maze, True)
                
                print(f"    Difficulty: {difficulty:.2f}")
                for format in output_formats:
                    if format in output_functions:
                        print(f"    Maze saved in {format.upper()} format (both solved and unsolved versions)")
        
        # Print statistics only if print_stats is True
        if print_stats:
            avg_difficulty = sum(difficulties) / len(difficulties)
            min_difficulty = min(difficulties)
            max_difficulty = max(difficulties)
            print(f"\nStatistics for {algorithm} algorithm:")
            print(f"    Average Difficulty: {avg_difficulty:.2f}")
            print(f"    Minimum Difficulty: {min_difficulty:.2f}")
            print(f"    Maximum Difficulty: {max_difficulty:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate mazes with specified algorithms and output formats.")
    parser.add_argument("-w", "--width", type=int, default=10, help="Width of the maze")
    parser.add_argument("--height", type=int, default=10, help="Height of the maze")
    parser.add_argument("-a", "--algorithms", nargs='+', default=['pri'], 
                        choices=list(ALGO_MAP.keys()) + list(ALGO_MAP.values()),
                        metavar="ALGO",
                        help="Algorithms to use for maze generation. Can use short names or full names. "
                             "Short names: " + ", ".join(ALGO_MAP.keys()) + ". "
                             "Full names: " + ", ".join(set(ALGO_MAP.values())))
    parser.add_argument("-f", "--formats", nargs='+', default=['png'], 
                        choices=['svg', 'png', 'gcode'], help="Output formats for the maze")
    parser.add_argument("-n", "--num_mazes", type=int, default=1, help="Number of mazes to generate for each algorithm")
    parser.add_argument("--no_output", action="store_true", help="Do not generate output files, only calculate difficulties")
    parser.add_argument("--print_stats", action="store_true", help="Print statistics for each algorithm")
    
    args = parser.parse_args()
    
    # Convert short algorithm names to full names
    algorithms = [ALGO_MAP.get(algo, algo) for algo in args.algorithms]
    
    generate_maze(args.width, args.height, algorithms, args.formats, args.num_mazes, not args.no_output, args.print_stats)