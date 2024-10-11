# Multi-Algorithm Maze Generator

This project is a Python-based maze generator that uses multiple algorithms to create and solve mazes. It supports various maze generation algorithms and can output mazes in different formats.

## Project Structure

The project is organized into several Python files:

- `main.py`: The main entry point of the application. It handles the generation of mazes using different algorithms and saves them in various formats.
- `maze.py`: Contains the `Maze` class, which represents the maze structure and includes methods for maze manipulation and visualization.
- `maze_algorithms.py`: Implements various maze generation algorithms.
- `utils.py`: Provides utility functions for saving mazes in different formats.

## Features

- Generate mazes using multiple algorithms, including DFS, Kruskal's, Prim's, and many more
- Calculate maze difficulty
- Save mazes in SVG, PNG, and GCode formats
- Generate both solved and unsolved versions of each maze
- Customizable maze size and number of mazes to generate
- Option to print statistics for generated mazes

## Usage

To generate mazes, run the following command:

```
python main.py [options]
```

### Command-line Options

- `-w`, `--width`: Width of the maze (default: 10)
- `--height`: Height of the maze (default: 10)
- `-a`, `--algorithms`: Algorithms to use for maze generation. Can use short names or full names. (default: ['pri'])
  - Short names: dfs, kru, pri, rd, ab, wil, hk, ell, sw, bt, gt, rb, ca, kw, abo
  - Full names: dfs, kruskal, prim, recursive_division, aldous_broder, wilsons, hunt_and_kill, ellers, sidewinder, binary_tree, growing_tree, recursive_backtracker, cellular_automata, kruskal_weighted, aldous_broder_optimized
- `-f`, `--formats`: Output formats for the maze (choices: svg, png, gcode; default: ['png'])
- `-n`, `--num_mazes`: Number of mazes to generate for each algorithm (default: 1)
- `--no_output`: Do not generate output files, only calculate difficulties
- `--print_stats`: Print statistics for each algorithm

### Examples

Generate a 20x20 maze using Prim's algorithm and save it as PNG:
```
python main.py -w 20 --height 20 -a pri -f png
```

Generate 5 mazes each using DFS and Kruskal's algorithms, save as SVG and PNG, and print statistics:
```
python main.py -a dfs kru -f svg png -n 5 --print_stats
```

Generate mazes using all available algorithms without saving output files, just print statistics:
```
python main.py -a dfs kru pri rd ab wil hk ell sw bt gt rb ca kw abo --no_output --print_stats
```

## Customization

You can customize the maze generation by modifying the parameters in the command-line arguments as shown in the usage section.

## Requirements

This project requires the following Python libraries:

- cairosvg (for SVG to PNG conversion)

You can install the required libraries using pip:

```
pip install cairosvg
```

## Version Control

This project is version controlled using Git. The `.gitignore` file is set up to exclude:

- The `oldtests/` directory
- Python virtual environments (`.venv/`)
- Python cache files and compiled bytecode
- IDE and editor-specific files
- OS-generated files
- Logs and databases
- Build output directories

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is open-source and available under the MIT License.
