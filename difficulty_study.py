"""
Extensive difficulty vs size scaling study across all maze algorithms.
Generates scatter charts and statistical analysis.
"""
import os
import sys
import csv
import time
import random
import importlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from maze import Maze

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Algorithms are tiered by speed to avoid hour-long waits
FAST_SIZES  = [5, 8, 10, 12, 15, 18, 20, 25, 30, 35, 40, 50, 60, 75, 100]
MED_SIZES   = [5, 8, 10, 12, 15, 18, 20, 25, 30, 35, 40, 50, 60, 75]
SLOW_SIZES  = [5, 8, 10, 12, 15, 18, 20, 25, 30, 35, 40, 50]

RUNS_PER_COMBO = 20   # runs per (algorithm, size) pair

SLOW_ALGOS = {'wilsons', 'hunt_and_kill', 'aldous_broder', 'cellular_automata'}
MED_ALGOS  = {'ellers', 'kruskal_weighted', 'randomized_prufer'}
SKIP_ALGOS = {'maze_from_image', 'recursive_division'}  # crash / need input

CSV_FILE = 'difficulty_study_data.csv'

# ---------------------------------------------------------------------------
# Load algorithms
# ---------------------------------------------------------------------------

def load_algorithms():
    algos = {}
    algorithm_dir = os.path.join(os.path.dirname(__file__), 'algorithms')
    for filename in sorted(os.listdir(algorithm_dir)):
        if filename.endswith('.py') and not filename.startswith('__'):
            name = filename[:-3]
            if name in SKIP_ALGOS:
                continue
            module = importlib.import_module(f'algorithms.{name}')
            func = getattr(module, f'generate_{name}', None)
            if func:
                algos[name] = func
    return algos

# ---------------------------------------------------------------------------
# Data collection
# ---------------------------------------------------------------------------

def collect_data(algos):
    rows = []
    plan = []
    for name in algos:
        if name in SLOW_ALGOS:
            sizes = SLOW_SIZES
        elif name in MED_ALGOS:
            sizes = MED_SIZES
        else:
            sizes = FAST_SIZES
        for size in sizes:
            for run in range(RUNS_PER_COMBO):
                plan.append((name, size, run))

    total = len(plan)
    print(f"Total runs planned: {total}")
    t0 = time.time()

    for i, (name, size, run) in enumerate(plan):
        seed = size * 10000 + run
        random.seed(seed)
        maze = Maze(size, size, name, algos[name])
        maze.generate()
        path = maze.find_path()
        diff = maze.calculate_difficulty()
        path_len = len(path) if path else 0
        solvable = path is not None

        rows.append({
            'algorithm': name,
            'size': size,
            'run': run,
            'difficulty': diff,
            'path_length': path_len,
            'solvable': solvable,
        })

        if (i + 1) % 200 == 0 or i + 1 == total:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            eta = (total - i - 1) / rate
            print(f"  [{i+1:5d}/{total}] {elapsed:6.1f}s elapsed, ~{eta:.0f}s remaining  "
                  f"(last: {name} {size}x{size})")

    print(f"Done collecting in {time.time()-t0:.1f}s")
    return rows

def save_csv(rows):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['algorithm','size','run','difficulty','path_length','solvable'])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {CSV_FILE}")

def load_csv():
    rows = []
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for r in reader:
            r['size'] = int(r['size'])
            r['run'] = int(r['run'])
            r['difficulty'] = float(r['difficulty'])
            r['path_length'] = int(r['path_length'])
            r['solvable'] = r['solvable'] == 'True'
            rows.append(r)
    return rows

# ---------------------------------------------------------------------------
# Chart helpers
# ---------------------------------------------------------------------------

# Use a dark style for high contrast
plt.style.use('dark_background')

# Hand-picked high-contrast palette (18 algorithms, all distinct on dark bg)
_PALETTE = [
    '#ff4444',  # red
    '#44bbff',  # sky blue
    '#44ff44',  # green
    '#ffaa00',  # orange
    '#ff44ff',  # magenta
    '#00ffcc',  # teal
    '#ffff44',  # yellow
    '#ff8888',  # salmon
    '#8888ff',  # periwinkle
    '#88ff88',  # light green
    '#ff6600',  # dark orange
    '#cc44ff',  # purple
    '#00ccff',  # cyan
    '#ffcc44',  # gold
    '#ff4488',  # hot pink
    '#44ffaa',  # mint
    '#aaaaff',  # lavender
    '#ffaacc',  # pink
    '#66ddff',  # light blue
    '#ddff66',  # lime
]

ALGO_COLORS = {}
def get_color(name):
    if name not in ALGO_COLORS:
        ALGO_COLORS[name] = _PALETTE[len(ALGO_COLORS) % len(_PALETTE)]
    return ALGO_COLORS[name]

def pretty_name(name):
    return name.replace('_', ' ').title()

# Common axis styling
def style_ax(ax, xlabel='', ylabel='', title='', fontsize_title=11):
    ax.set_xlabel(xlabel, fontsize=10, color='#cccccc')
    ax.set_ylabel(ylabel, fontsize=10, color='#cccccc')
    if title:
        ax.set_title(title, fontsize=fontsize_title, fontweight='bold', color='white')
    ax.tick_params(colors='#aaaaaa', labelsize=8)
    ax.grid(True, alpha=0.2, color='#555555')
    for spine in ax.spines.values():
        spine.set_color('#444444')

# ---------------------------------------------------------------------------
# Chart 1: Scatter grid — one subplot per algorithm
# ---------------------------------------------------------------------------

def chart_scatter_grid(rows):
    algo_names = sorted(set(r['algorithm'] for r in rows))
    n = len(algo_names)
    cols = 4
    nrows = (n + cols - 1) // cols

    fig, axes = plt.subplots(nrows, cols, figsize=(22, 4.5 * nrows),
                             squeeze=False, facecolor='#1a1a2e')
    fig.suptitle('Maze Difficulty vs Size — Per Algorithm',
                 fontsize=18, fontweight='bold', color='white', y=1.01)

    for idx, name in enumerate(algo_names):
        ax = axes[idx // cols][idx % cols]
        ax.set_facecolor('#1a1a2e')
        data = [r for r in rows if r['algorithm'] == name]
        sizes = [r['size'] for r in data]
        diffs = [r['difficulty'] for r in data]
        color = get_color(name)
        ax.scatter(sizes, diffs, s=18, alpha=0.7, color=color, edgecolors='none')

        # Fit quadratic trendline
        if len(sizes) > 3:
            s_arr = np.array(sizes)
            d_arr = np.array(diffs)
            coeffs = np.polyfit(s_arr, d_arr, 2)
            x_fit = np.linspace(min(sizes), max(sizes), 100)
            y_fit = np.polyval(coeffs, x_fit)
            ax.plot(x_fit, y_fit, color='white', linewidth=2, alpha=0.8)

        style_ax(ax, 'Size', 'Difficulty', pretty_name(name))
        ax.set_ylim(-0.02, 0.85)

    for idx in range(n, nrows * cols):
        axes[idx // cols][idx % cols].set_visible(False)

    fig.tight_layout()
    fig.savefig('study_scatter_grid.png', dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print("Saved study_scatter_grid.png")
    plt.close(fig)

# ---------------------------------------------------------------------------
# Chart 2: All algorithms overlaid — mean with error bands
# ---------------------------------------------------------------------------

def chart_overlay(rows):
    algo_names = sorted(set(r['algorithm'] for r in rows))

    fig, ax = plt.subplots(figsize=(16, 10), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    fig.suptitle('Mean Difficulty vs Size — All Algorithms',
                 fontsize=16, fontweight='bold', color='white')

    for name in algo_names:
        data = [r for r in rows if r['algorithm'] == name]
        by_size = {}
        for r in data:
            by_size.setdefault(r['size'], []).append(r['difficulty'])

        sizes = sorted(by_size.keys())
        means = [np.mean(by_size[s]) for s in sizes]
        stds  = [np.std(by_size[s]) for s in sizes]
        color = get_color(name)

        ax.plot(sizes, means, marker='o', markersize=5, linewidth=2,
                label=pretty_name(name), color=color)
        ax.fill_between(sizes,
                         [m - s for m, s in zip(means, stds)],
                         [m + s for m, s in zip(means, stds)],
                         alpha=0.18, color=color)

    style_ax(ax, 'Maze Size (width = height)', 'Difficulty Score (0–1)')
    legend = ax.legend(fontsize=9, ncol=3, loc='upper left',
                       facecolor='#2a2a3e', edgecolor='#555555',
                       labelcolor='white', framealpha=0.9)
    fig.tight_layout()
    fig.savefig('study_overlay.png', dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print("Saved study_overlay.png")
    plt.close(fig)

# ---------------------------------------------------------------------------
# Chart 3: Algorithm ranking — horizontal bar chart of mean difficulty
# ---------------------------------------------------------------------------

def chart_normalized(rows):
    algo_names = sorted(set(r['algorithm'] for r in rows))

    # Compute mean ± std across all sizes for each algorithm
    stats = {}
    for name in algo_names:
        diffs = [r['difficulty'] for r in rows if r['algorithm'] == name]
        stats[name] = (np.mean(diffs), np.std(diffs))

    # Sort by mean difficulty descending
    ranked = sorted(stats.items(), key=lambda x: x[1][0], reverse=True)
    names = [pretty_name(n) for n, _ in ranked]
    means = [v[0] for _, v in ranked]
    stds = [v[1] for _, v in ranked]
    colors = [get_color(n) for n, _ in ranked]

    fig, ax = plt.subplots(figsize=(14, 10), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    fig.suptitle('Algorithm Difficulty Ranking (0–1 scale)',
                 fontsize=16, fontweight='bold', color='white')

    y_pos = np.arange(len(names))
    bars = ax.barh(y_pos, means, xerr=stds, height=0.7, color=colors,
                   edgecolor='none', capsize=3, error_kw={'color': '#aaaaaa',
                   'linewidth': 1.2})

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=10, color='white')
    ax.invert_yaxis()
    ax.set_xlim(0, 0.7)
    style_ax(ax, 'Mean Difficulty Score', '')

    # Add value labels on bars
    for i, (m, s) in enumerate(zip(means, stds)):
        ax.text(m + s + 0.01, i, f'{m:.3f}', va='center', fontsize=9,
                color='#cccccc')

    fig.tight_layout()
    fig.savefig('study_normalized.png', dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print("Saved study_normalized.png")
    plt.close(fig)

# ---------------------------------------------------------------------------
# Chart 4: Path length vs size scatter grid
# ---------------------------------------------------------------------------

def chart_path_length_grid(rows):
    algo_names = sorted(set(r['algorithm'] for r in rows))
    n = len(algo_names)
    cols = 4
    nrows_grid = (n + cols - 1) // cols

    fig, axes = plt.subplots(nrows_grid, cols, figsize=(22, 4.5 * nrows_grid),
                             squeeze=False, facecolor='#1a1a2e')
    fig.suptitle('Solution Path Length vs Size — Per Algorithm',
                 fontsize=18, fontweight='bold', color='white', y=1.01)

    for idx, name in enumerate(algo_names):
        ax = axes[idx // cols][idx % cols]
        ax.set_facecolor('#1a1a2e')
        data = [r for r in rows if r['algorithm'] == name and r['solvable']]
        sizes = [r['size'] for r in data]
        plens = [r['path_length'] for r in data]
        color = get_color(name)

        ax.scatter(sizes, plens, s=18, alpha=0.7, color=color, edgecolors='none')

        if sizes:
            x_ref = np.linspace(min(sizes), max(sizes), 100)
            ax.plot(x_ref, x_ref ** 2, color='#888888', linewidth=1.5,
                    alpha=0.5, linestyle='--', label='size²')

        style_ax(ax, 'Size', 'Path Length', pretty_name(name))

    for idx in range(n, nrows_grid * cols):
        axes[idx // cols][idx % cols].set_visible(False)

    fig.tight_layout()
    fig.savefig('study_path_length_grid.png', dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print("Saved study_path_length_grid.png")
    plt.close(fig)

# ---------------------------------------------------------------------------
# Chart 5: Difficulty variance (coefficient of variation) per algorithm
# ---------------------------------------------------------------------------

def chart_variance(rows):
    algo_names = sorted(set(r['algorithm'] for r in rows))

    fig, ax = plt.subplots(figsize=(16, 10), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    fig.suptitle('Difficulty Coefficient of Variation vs Size',
                 fontsize=16, fontweight='bold', color='white')

    for name in algo_names:
        data = [r for r in rows if r['algorithm'] == name]
        by_size = {}
        for r in data:
            by_size.setdefault(r['size'], []).append(r['difficulty'])

        sizes = sorted(by_size.keys())
        cvs = []
        for s in sizes:
            vals = by_size[s]
            m = np.mean(vals)
            cv = np.std(vals) / m if m > 0 else 0
            cvs.append(cv)

        ax.plot(sizes, cvs, marker='o', markersize=5, linewidth=2,
                label=pretty_name(name), color=get_color(name))

    style_ax(ax, 'Maze Size', 'CV (σ / μ)')
    legend = ax.legend(fontsize=9, ncol=3, loc='upper right',
                       facecolor='#2a2a3e', edgecolor='#555555',
                       labelcolor='white', framealpha=0.9)
    fig.tight_layout()
    fig.savefig('study_variance.png', dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print("Saved study_variance.png")
    plt.close(fig)

# ---------------------------------------------------------------------------
# Chart 6: Log-log scatter to identify power-law exponents
# ---------------------------------------------------------------------------

def chart_loglog(rows):
    algo_names = sorted(set(r['algorithm'] for r in rows))
    n = len(algo_names)
    cols = 4
    nrows_grid = (n + cols - 1) // cols

    fig, axes = plt.subplots(nrows_grid, cols, figsize=(22, 4.5 * nrows_grid),
                             squeeze=False, facecolor='#1a1a2e')
    fig.suptitle('Log-Log Difficulty vs Size — Power Law Fit',
                 fontsize=18, fontweight='bold', color='white', y=1.01)

    for idx, name in enumerate(algo_names):
        ax = axes[idx // cols][idx % cols]
        ax.set_facecolor('#1a1a2e')
        data = [r for r in rows if r['algorithm'] == name and r['difficulty'] > 0]
        sizes = np.array([r['size'] for r in data], dtype=float)
        diffs = np.array([r['difficulty'] for r in data], dtype=float)
        color = get_color(name)

        ax.scatter(sizes, diffs, s=18, alpha=0.7, color=color, edgecolors='none')

        if len(sizes) > 3:
            log_s = np.log(sizes)
            log_d = np.log(diffs)
            coeffs = np.polyfit(log_s, log_d, 1)
            exponent = coeffs[0]
            x_fit = np.linspace(sizes.min(), sizes.max(), 100)
            y_fit = np.exp(np.polyval(coeffs, np.log(x_fit)))
            ax.plot(x_fit, y_fit, color='white', linewidth=2, alpha=0.8)
            ax.text(0.05, 0.92, f'exp ≈ {exponent:.2f}',
                    transform=ax.transAxes, fontsize=9, verticalalignment='top',
                    color='white',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#333355', alpha=0.9,
                              edgecolor='#666688'))

        ax.set_xscale('log')
        ax.set_yscale('log')
        style_ax(ax, 'Size (log)', 'Difficulty (log)', pretty_name(name))
        ax.grid(True, alpha=0.15, color='#555555', which='both')

    for idx in range(n, nrows_grid * cols):
        axes[idx // cols][idx % cols].set_visible(False)

    fig.tight_layout()
    fig.savefig('study_loglog.png', dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print("Saved study_loglog.png")
    plt.close(fig)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    algos = load_algorithms()
    print(f"Loaded {len(algos)} algorithms: {', '.join(algos.keys())}")

    # Collect or load data
    if os.path.exists(CSV_FILE) and '--regenerate' not in sys.argv:
        print(f"Loading existing data from {CSV_FILE}...")
        rows = load_csv()
        print(f"Loaded {len(rows)} rows")
    else:
        rows = collect_data(algos)
        save_csv(rows)

    # Generate all charts
    print("\nGenerating charts...")
    chart_scatter_grid(rows)
    chart_overlay(rows)
    chart_normalized(rows)
    chart_path_length_grid(rows)
    chart_variance(rows)
    chart_loglog(rows)
    print("\nAll done!")
