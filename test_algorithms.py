import time
import signal
import os
import importlib
from maze import Maze

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Algorithm execution timed out")

# Dynamically import all algorithm modules
algorithm_modules = {}
algorithm_dir = os.path.join(os.path.dirname(__file__), 'algorithms')
for filename in os.listdir(algorithm_dir):
    if filename.endswith('.py') and not filename.startswith('__'):
        module_name = filename[:-3]  # Remove .py extension
        module = importlib.import_module(f'algorithms.{module_name}')
        algorithm_modules[module_name] = module

def test_all_algorithms():
    width = 30
    height = 30
    algorithms = list(algorithm_modules.keys())
    num_mazes = 1
    timeout_seconds = 60

    print(f"Testing all maze algorithms with a {width}x{height} maze:")
    
    for algorithm in algorithms:
        print(f"\nTesting {algorithm}...")
        start_time = time.time()
        
        # Set the signal handler and a 60-second alarm
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_seconds)
        
        try:
            generate_func = getattr(algorithm_modules[algorithm], f'generate_{algorithm}')
            if algorithm == 'maze_from_image':
                # Create a test image for maze_from_image
                from create_test_image import create_test_image
                test_image_path = 'test_image.png'
                create_test_image(test_image_path, width, height)
                maze = Maze(width, height, algorithm, lambda m: generate_func(m, test_image_path))
            else:
                maze = Maze(width, height, algorithm, generate_func)
            maze.generate()
            execution_time = time.time() - start_time
            print(f"✅ {algorithm} test passed. Execution time: {execution_time:.2f} seconds")
        except TimeoutException:
            print(f"❌ {algorithm} test failed. Execution timed out after {timeout_seconds} seconds")
        except Exception as e:
            print(f"❌ {algorithm} test failed. Error: {str(e)}")
        finally:
            # Cancel the alarm
            signal.alarm(0)

def test_maze_difficulty():
    width = 30
    height = 30
    algorithms = list(algorithm_modules.keys())
    num_tests = 5

    print(f"\nTesting maze difficulty calculation for all algorithms:")
    
    for algorithm in algorithms:
        print(f"\nTesting {algorithm}...")
        difficulties = []
        
        generate_func = getattr(algorithm_modules[algorithm], f'generate_{algorithm}')
        
        for _ in range(num_tests):
            if algorithm == 'maze_from_image':
                # Create a test image for maze_from_image
                from create_test_image import create_test_image
                test_image_path = 'test_image.png'
                create_test_image(test_image_path, width, height)
                maze = Maze(width, height, algorithm, lambda m: generate_func(m, test_image_path))
            else:
                maze = Maze(width, height, algorithm, generate_func)
            maze.generate()
            
            difficulty = maze.calculate_difficulty()
            difficulties.append(difficulty)
            print(f"Difficulty: {difficulty:.4f}")
        
        avg_difficulty = sum(difficulties) / len(difficulties)
        print(f"Average difficulty for {algorithm}: {avg_difficulty:.4f}")

if __name__ == "__main__":
    test_all_algorithms()
    test_maze_difficulty()
