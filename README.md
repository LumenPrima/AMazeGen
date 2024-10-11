# Multi-Algorithm Maze Generator

This project is a Python-based maze generator that uses multiple algorithms to create and solve mazes. It can generate mazes using three different algorithms: Depth-First Search (DFS), Kruskal's algorithm, and Prim's algorithm.

## Project Structure

The project is organized into several Python files:

- `main.py`: The main entry point of the application. It handles the generation of mazes using different algorithms and saves them in various formats.
- `maze.py`: Contains the `Maze` class, which represents the maze structure and includes methods for maze manipulation and visualization.
- `maze_algorithms.py`: Implements the three maze generation algorithms (DFS, Kruskal, and Prim).
- `disjoint_set.py`: Contains the `DisjointSet` class used in Kruskal's algorithm.
- `utils.py`: Provides utility functions for saving mazes as SVG and PNG files.

## Features

- Generate mazes using three different algorithms: DFS, Kruskal, and Prim
- Calculate maze difficulty
- Save mazes in both SVG and PNG formats
- Generate both solved and unsolved versions of each maze

## Usage

To generate mazes using all three algorithms, run the following command:

```
python main.py
```

This will create mazes with a size of 10x10 using each algorithm and save them in both SVG and PNG formats.

## Customization

You can customize the maze generation by modifying the parameters in the `main.py` file:

- Change the maze size by modifying the `width` and `height` parameters in the `generate_maze` function call.
- Adjust the output formats by modifying the `output_formats` parameter.
- Generate mazes using specific algorithms by modifying the `algo` list in the main execution loop.

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
