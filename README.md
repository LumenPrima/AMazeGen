# Multi-Algorithm Maze Generator

Welcome to the Multi-Algorithm Maze Generator! This Python-based project offers a versatile toolkit for generating, visualizing, and analyzing mazes using a variety of algorithms. Whether you're a maze enthusiast, a computer science student studying algorithms, or a developer looking for a robust maze generation library, this project has something for you.

## Project Overview

This maze generator implements multiple algorithms to create diverse maze structures. It also provides tools for maze visualization, difficulty calculation, and even physical representation through G-code output. The project now supports dynamic loading of algorithm modules, allowing users to easily add their own custom algorithms.

## Project Structure

The project is organized into several Python files:

- `main.py`: The main entry point of the application. It handles the dynamic loading of algorithms and the generation of mazes using different algorithms, saving them in various formats.
- `maze.py`: Contains the `Maze` class, which represents the maze structure and includes methods for maze manipulation and visualization.
- `utils.py`: Provides utility functions for saving mazes in different formats.
- `disjoint_set.py`: Implements the DisjointSet data structure used in some maze generation algorithms.
- `algorithms/`: A directory containing individual Python files for each maze generation algorithm.

## Features

- Generate mazes using multiple algorithms, including:
  - Depth-First Search (DFS)
  - Kruskal's Algorithm
  - Prim's Algorithm
  - Recursive Division
  - Aldous-Broder Algorithm
  - Wilson's Algorithm
  - Hunt-and-Kill Algorithm
  - Eller's Algorithm
  - Sidewinder Algorithm
  - Binary Tree Algorithm
  - Growing Tree Algorithm
  - Recursive Backtracker
  - Cellular Automata
  - Weighted Kruskal's Algorithm
  - Optimized Aldous-Broder Algorithm
  - Image-based Maze Generation
  - Spiral Backtracker Algorithm
  - Fractal Recursive Division Algorithm
  - Braid Maze Generator
  - Randomized Prüfer Algorithm
  - Quad-tree Maze Generation
- Dynamic loading of algorithm modules, allowing easy addition of custom algorithms
- Calculate maze difficulty based on various factors
- Save mazes in SVG, PNG, and GCode formats
- Generate both solved and unsolved versions of each maze
- Customizable maze size and number of mazes to generate
- Option to print statistics for generated mazes
- Set custom start and end points for mazes
- Specify a random seed for reproducible maze generation
- Adjust cell size for visual customization

## Maze Generation Algorithms

Each algorithm produces mazes with unique characteristics. For detailed descriptions of each algorithm, please refer to the individual algorithm files in the `algorithms/` directory.

## Adding Custom Algorithms

To add your own maze generation algorithm:

1. Create a new Python file in the `algorithms/` directory.
2. Name your file descriptively, e.g., `my_custom_algorithm.py`.
3. In the file, define a function named `generate_my_custom_algorithm(maze)` where `maze` is an instance of the `Maze` class.
4. Implement your algorithm within this function, modifying the `maze.grid` to create the maze structure.
5. Save the file.

The main application will automatically detect and include your new algorithm at runtime.

## Maze Difficulty Calculation

The project includes a method to calculate maze difficulty based on several factors:

- Path length: Longer solutions increase difficulty.
- Number of dead ends: More dead ends make a maze more challenging.
- Number of intersections: More choices at intersections increase complexity.
- Maze density: Denser mazes with more walls are generally more difficult.

## Output Formats

- SVG: Scalable Vector Graphics format, ideal for web display or further editing.
- PNG: Raster image format, good for direct viewing or printing.
- GCode: Can be used with CNC machines or 3D printers to physically create the maze.

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/multi-algorithm-maze-generator.git
   cd multi-algorithm-maze-generator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the maze generator:
   ```
   python main.py [options]
   ```

## Usage

To generate mazes, run the following command:

```
python main.py [options]
```

### Command-line Options

- `-x`, `--width`: Width of the maze (x-axis) (default: 10)
- `-y`, `--height`: Height of the maze (y-axis) (default: 10)
- `-a`, `--algorithms`: Algorithms to use for maze generation. Can use short names, full names, or 'all'.
- `-f`, `--formats`: Output formats for the maze (choices: svg, png, gcode; default: ['png'])
- `-n`, `--num_mazes`: Number of mazes to generate for each algorithm (default: 1)
- `--no_output`: Do not generate output files, only calculate difficulties
- `--print_stats`: Print statistics for each algorithm
- `--image_path`: Path to the image file for maze_from_image algorithm
- `-o`, `--output_dir`: Directory to save output files (default: './output')
- `--seed`: Seed for random number generator (for reproducible maze generation)
- `--start`: Start point coordinates (x y)
- `--end`: End point coordinates (x y)
- `--cell_size`: Cell size in pixels for SVG and PNG output (default: 10)

The available algorithms are dynamically loaded from the `algorithms/` directory. Use the algorithm's filename (without the .py extension) as the full name, or use the short name generated as follows:
- For single-word algorithm names: The first three letters of the name (e.g., 'pri' for 'prim').
- For multi-word algorithm names: The first letter of each word (e.g., 'mfi' for 'maze_from_image').

### Examples

Generate a 20x20 maze using Prim's algorithm and save it as PNG:
```
python main.py -x 20 -y 20 -a pri -f png
```

Generate 5 mazes each using DFS and Kruskal's algorithms, save as SVG and PNG, and print statistics:
```
python main.py -a dfs kru -f svg png -n 5 --print_stats
```

Generate a maze from an image:
```
python main.py -a mfi --image_path path/to/your/image.png
```

Generate mazes using all available algorithms without saving output files, just print statistics:
```
python main.py -a all --no_output --print_stats
```

Generate a maze with custom start and end points, and a specific random seed:
```
python main.py -x 30 -y 30 -a dfs --start 0 0 --end 29 29 --seed 12345
```

Generate a maze with larger cell size for better visibility:
```
python main.py -x 15 -y 15 -a kru --cell_size 20
```

## Customization

You can customize the maze generation by modifying the parameters in the command-line arguments as shown in the usage section. To add your own algorithms, simply place a new Python file in the `algorithms/` directory following the naming convention described in the "Adding Custom Algorithms" section.

## Dependencies

This project requires the following Python libraries:

- cairosvg (for SVG to PNG conversion)
- Pillow (for image processing in image-based maze generation)

The full list of dependencies can be found in the `requirements.txt` file.

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
