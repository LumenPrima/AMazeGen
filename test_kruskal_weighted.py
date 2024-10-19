from maze import Maze
from algorithms.kruskal_weighted import generate_kruskal_weighted
from utils import svg_to_png
import os

def test_kruskal_weighted():
    width, height = 30, 30
    maze = Maze(width, height, "kruskal_weighted", generate_kruskal_weighted)
    maze.generate_func(maze)
    
    svg_content = maze.to_svg()
    print("SVG content generated successfully")
    print(f"SVG content length: {len(svg_content)}")
    print("First 100 characters of SVG content:")
    print(svg_content[:100])
    
    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)
    
    svg_filename = os.path.join(output_dir, 'test_kruskal_weighted.svg')
    with open(svg_filename, 'w') as f:
        f.write(svg_content)
    print(f"SVG file saved: {svg_filename}")
    
    png_filename = os.path.join(output_dir, 'test_kruskal_weighted.png')
    try:
        svg_to_png(svg_content, png_filename, width=800, height=800)
        print(f"PNG file saved: {png_filename}")
    except Exception as e:
        print(f"Error converting SVG to PNG: {str(e)}")
        print("Full SVG content:")
        print(svg_content)

if __name__ == "__main__":
    test_kruskal_weighted()
