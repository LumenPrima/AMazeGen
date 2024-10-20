import os
import importlib
import random
import matplotlib.pyplot as plt
import csv
import time
from maze import Maze
from main import ALGO_MAP, generate_maze

def plot_difficulty_vs_size(sizes, num_mazes_per_size):
    algorithms = [(name, func) for name, func in ALGO_MAP.values() if name != 'maze_from_image']
    results = {algo[0]: {size: [] for size in sizes} for algo in algorithms}
    total_iterations = len(sizes) * len(algorithms) * num_mazes_per_size
    current_iteration = 0

    start_time = time.time()

    for size in sizes:
        print(f"\nGenerating mazes of size {size}x{size}")
        for algo_name, generate_func in algorithms:
            difficulties = []
            for i in range(num_mazes_per_size):
                current_iteration += 1
                try:
                    print(f"\rProgress: {current_iteration}/{total_iterations} ({current_iteration/total_iterations*100:.2f}%) - Current: {algo_name}, Size: {size}x{size}, Maze: {i+1}/{num_mazes_per_size}", end="", flush=True)
                    maze = Maze(size, size, algo_name, generate_func)
                    maze.generate()
                    difficulty = maze.calculate_difficulty()
                    difficulties.append(difficulty)
                except Exception as e:
                    print(f"\nError generating maze with {algo_name} algorithm: {str(e)}")
                    continue
            if difficulties:
                avg_difficulty = sum(difficulties) / len(difficulties)
                results[algo_name][size] = avg_difficulty
            else:
                print(f"\nWarning: No valid mazes generated for {algo_name} at size {size}x{size}")

    end_time = time.time()
    print(f"\n\nTotal execution time: {end_time - start_time:.2f} seconds")

    # Plotting
    plt.figure(figsize=(12, 8))
    for algo_name in results:
        sizes_list = list(results[algo_name].keys())
        difficulties_list = list(results[algo_name].values())
        if difficulties_list:  # Only plot if we have data
            plt.plot(sizes_list, difficulties_list, marker='o', label=algo_name)

    plt.xlabel('Maze Size')
    plt.ylabel('Average Difficulty')
    plt.title('Average Difficulty vs Maze Size for Different Algorithms')
    plt.legend()
    plt.grid(True)
    plt.savefig('difficulty_vs_size_plot.png')
    print("Plot saved as 'difficulty_vs_size_plot.png'")
    
    # Display plot if in interactive environment
    if hasattr(plt, 'show'):
        plt.show()
    else:
        plt.close()

    # Save numerical data to CSV
    with open('difficulty_vs_size_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Algorithm'] + [f'Size {size}x{size}' for size in sizes]
        writer.writerow(header)
        for algo_name, size_data in results.items():
            row = [algo_name] + [size_data.get(size, '') for size in sizes]
            writer.writerow(row)

    print("Numerical data saved as 'difficulty_vs_size_data.csv'")

if __name__ == "__main__":
    sizes = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80]  # Extended range of sizes
    num_mazes_per_size = 5  # You can adjust this number
    plot_difficulty_vs_size(sizes, num_mazes_per_size)
