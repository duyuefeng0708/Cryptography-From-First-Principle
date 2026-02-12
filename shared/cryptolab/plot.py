"""
Matplotlib visualization wrappers replacing SageMath plotting primitives.

Provides: Cayley graphs, cycle diagrams, subgroup lattices,
multiplication heatmaps, coset coloring, and graphics arrays.

All functions use matplotlib (Pyodide-compatible).
"""

import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np


# ---------------------------------------------------------------------------
# Cayley graph (replaces DiGraph().plot(layout='circular'))
# ---------------------------------------------------------------------------

def cayley_graph(n, generator, op='add', figsize=5, vertex_color='lightblue',
                 edge_color='steelblue', vertex_size=500, title=None, ax=None):
    """
    Draw a Cayley graph for Z/nZ with the given generator.

    op='add': additive group, arrow from a to (a + generator) mod n
    op='mul': multiplicative group, arrow from a to (a * generator) mod n
              Only draws edges for the given elements.

    Returns the matplotlib Figure (or None if ax was provided).
    """
    show = ax is None
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(figsize, figsize))
    else:
        fig = ax.figure

    if op == 'add':
        elements = list(range(n))
    else:
        # For multiplicative, only use units
        from .number_theory import gcd
        elements = [a for a in range(1, n) if gcd(a, n) == 1]

    num = len(elements)
    # Place on circle
    angles = {elem: 2 * math.pi * i / num - math.pi / 2 for i, elem in enumerate(elements)}
    positions = {elem: (math.cos(angles[elem]), math.sin(angles[elem])) for elem in elements}

    # Draw edges (arrows)
    for a in elements:
        if op == 'add':
            target = (a + generator) % n
        else:
            target = (a * generator) % n
        if target not in positions:
            continue
        px, py = positions[a]
        cx, cy = positions[target]
        dx, dy = cx - px, cy - py
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0.01:
            shrink = 0.12
            ax.annotate(
                '', xy=(cx - shrink * dx / dist, cy - shrink * dy / dist),
                xytext=(px + shrink * dx / dist, py + shrink * dy / dist),
                arrowprops=dict(arrowstyle='->', color=edge_color, lw=1.5),
                zorder=2
            )

    # Draw nodes
    radius = 0.08
    for elem in elements:
        ex, ey = positions[elem]
        circ = plt.Circle((ex, ey), radius, facecolor=vertex_color,
                           edgecolor='gray', linewidth=1, zorder=3)
        ax.add_patch(circ)
        ax.text(ex, ey, str(elem), ha='center', va='center',
                fontsize=10, zorder=4)

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    if title:
        ax.set_title(title, fontsize=11)

    if show:
        plt.tight_layout()
        plt.show()
        return fig
    return None


# ---------------------------------------------------------------------------
# Cycle diagram (replaces Graphics() + circle + arrow + text in 01d)
# ---------------------------------------------------------------------------

def cycle_diagram(n, elements, generator, op='mul', figsize=5,
                  highlight_color='steelblue', title=None, ax=None):
    """
    Draw a cycle diagram showing the power/addition cycle of a generator.

    elements: the full list of group elements (placed on the circle)
    generator: the element whose cycle to highlight
    op: 'mul' for multiplicative, 'add' for additive

    Highlighted nodes are in the cycle, gray nodes are not reached.
    Returns the Figure (or None if ax was provided).
    """
    show = ax is None
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(figsize, figsize))
    else:
        fig = ax.figure

    num = len(elements)
    angles = {int(elem): 2 * math.pi * i / num - math.pi / 2
              for i, elem in enumerate(elements)}
    positions = {int(elem): (math.cos(angles[int(elem)]), math.sin(angles[int(elem)]))
                 for elem in elements}

    # Compute the cycle
    modulus = n
    if op == 'mul':
        cycle = []
        val = 1
        for _ in range(num):
            val = (val * generator) % modulus
            cycle.append(val)
            if val == 1:
                break
    else:
        cycle = []
        val = 0
        for _ in range(n):
            val = (val + generator) % modulus
            cycle.append(val)
            if val == 0:
                break

    cycle_set = set(cycle)

    # Draw all nodes (gray for non-cycle, highlighted for cycle)
    radius = 0.1
    for elem in elements:
        e = int(elem)
        ex, ey = positions[e]
        if e in cycle_set:
            fc = highlight_color
            tc = 'white'
            fw = 'bold'
        else:
            fc = 'lightgray'
            tc = 'black'
            fw = 'normal'
        circ = plt.Circle((ex, ey), radius, facecolor=fc,
                           edgecolor='white' if e in cycle_set else 'gray',
                           linewidth=1.5, zorder=5)
        ax.add_patch(circ)
        ax.text(ex, ey, str(e), ha='center', va='center',
                fontsize=10, fontweight=fw, color=tc, zorder=6)

    # Draw arrows along the cycle
    identity = 1 if op == 'mul' else 0
    prev_elem = identity
    for curr_elem in cycle:
        if prev_elem in positions and curr_elem in positions:
            px, py = positions[prev_elem]
            cx, cy = positions[curr_elem]
            dx, dy = cx - px, cy - py
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 0.01:
                shrink = 0.13
                ax.annotate(
                    '', xy=(cx - shrink * dx / dist, cy - shrink * dy / dist),
                    xytext=(px + shrink * dx / dist, py + shrink * dy / dist),
                    arrowprops=dict(arrowstyle='->', color=highlight_color,
                                    lw=1.5),
                    zorder=2
                )
        prev_elem = curr_elem

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    if title:
        ax.set_title(title, fontsize=10)

    if show:
        plt.tight_layout()
        plt.show()
        return fig
    return None


# ---------------------------------------------------------------------------
# Subgroup lattice (replaces Poset().plot())
# ---------------------------------------------------------------------------

def subgroup_lattice(n, figsize=6):
    """
    Draw the subgroup lattice of Z/nZ.
    Each node is labeled with the generator and the subgroup size.
    Lines connect subgroups where one contains the other (direct inclusion).
    Returns the Figure.
    """
    from .number_theory import divisors as get_divisors

    divs = get_divisors(n)
    # Vertical position by subgroup size (log scale for better spacing)
    y_pos = {d: math.log2(d) if d > 0 else 0 for d in divs}
    max_y = max(y_pos.values()) if y_pos else 1

    # Group divisors by their y level for horizontal spacing
    levels = {}
    for d in divs:
        y = y_pos[d]
        if y not in levels:
            levels[y] = []
        levels[y].append(d)

    positions = {}
    for y, ds in levels.items():
        count = len(ds)
        for i, d in enumerate(sorted(ds)):
            x = (i - (count - 1) / 2) * 1.5
            positions[d] = (x, y / max_y * 4 if max_y > 0 else 0)

    fig, ax = plt.subplots(1, 1, figsize=(figsize, figsize))

    # Draw edges (direct containment)
    for d1 in divs:
        for d2 in divs:
            if d2 <= d1 or d2 % d1 != 0:
                continue
            # Check for direct edge: no d3 strictly between d1 and d2
            if any(d1 < d3 < d2 and d2 % d3 == 0 and d3 % d1 == 0 for d3 in divs):
                continue
            x1, y1 = positions[d1]
            x2, y2 = positions[d2]
            ax.plot([x1, x2], [y1, y2], color='gray', linewidth=1, zorder=1)

    # Draw nodes
    for d in divs:
        x, y = positions[d]
        gen = n // d
        circ = plt.Circle((x, y), 0.3, facecolor='lightyellow',
                           edgecolor='black', linewidth=1.5, zorder=3)
        ax.add_patch(circ)
        ax.text(x, y + 0.07, f'<{gen}>', ha='center', va='center',
                fontsize=9, fontweight='bold', zorder=4)
        ax.text(x, y - 0.1, f'|{d}|', ha='center', va='center',
                fontsize=8, color='gray', zorder=4)

    margin = 1.0
    xs = [p[0] for p in positions.values()]
    ys = [p[1] for p in positions.values()]
    ax.set_xlim(min(xs) - margin, max(xs) + margin)
    ax.set_ylim(min(ys) - margin, max(ys) + margin)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'Subgroup lattice of (Z/{n}Z, +)', fontsize=12)

    plt.tight_layout()
    plt.show()
    return fig


# ---------------------------------------------------------------------------
# Multiplication heatmap (replaces matrix_plot())
# ---------------------------------------------------------------------------

def multiplication_heatmap(table, labels=None, cmap='viridis', figsize=5,
                           title=None):
    """
    Draw a heatmap of a multiplication (or addition) table.

    table: 2D list or numpy array of values
    labels: row/column labels (defaults to indices)
    cmap: matplotlib colormap name
    Returns the Figure.
    """
    arr = np.array(table)
    n = arr.shape[0]
    if labels is None:
        labels = list(range(n))

    fig, ax = plt.subplots(1, 1, figsize=(figsize, figsize))
    im = ax.imshow(arr, cmap=cmap, aspect='equal', origin='upper')

    ax.set_xticks(range(n))
    ax.set_xticklabels([str(l) for l in labels])
    ax.set_yticks(range(n))
    ax.set_yticklabels([str(l) for l in labels])

    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')

    if title:
        ax.set_title(title, fontsize=12, pad=15)

    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.show()
    return fig


# ---------------------------------------------------------------------------
# Coset coloring (replaces Graphics() + circle + text + parametric_plot)
# ---------------------------------------------------------------------------

def coset_coloring(n, subgroup_elements, figsize=5, title=None,
                   colors=None):
    """
    Draw elements of Z/nZ on a circle, colored by their coset membership.

    subgroup_elements: list of ints forming the subgroup H
    Colors are assigned per coset. Returns the Figure.
    """
    if colors is None:
        colors = ['royalblue', 'orangered', 'forestgreen', 'mediumorchid',
                  'goldenrod', 'crimson', 'teal', 'slateblue']

    H = [int(h) % n for h in subgroup_elements]
    H_set = set(H)

    # Assign cosets
    covered = set()
    cosets = []
    for a in range(n):
        if a in covered:
            continue
        coset = sorted(set((a + h) % n for h in H))
        cosets.append((a, coset))
        covered.update(coset)

    # Color mapping
    element_color = {}
    for idx, (rep, coset) in enumerate(cosets):
        c = colors[idx % len(colors)]
        for elem in coset:
            element_color[elem] = c

    fig, ax = plt.subplots(1, 1, figsize=(figsize, figsize))

    # Draw faint outline circle
    theta = np.linspace(0, 2 * math.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), color='lightgray', linewidth=0.5, zorder=1)

    # Draw elements
    radius = 0.1
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2
        cx, cy = math.cos(angle), math.sin(angle)
        circ = plt.Circle((cx, cy), radius, facecolor=element_color[i],
                           edgecolor='white', linewidth=2, zorder=3)
        ax.add_patch(circ)
        ax.text(cx, cy, str(i), ha='center', va='center',
                fontsize=11, fontweight='bold', color='white', zorder=4)

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    if title:
        ax.set_title(title, fontsize=12)

    plt.tight_layout()
    plt.show()
    return fig


# ---------------------------------------------------------------------------
# Graphics array (replaces SageMath's graphics_array())
# ---------------------------------------------------------------------------

def graphics_array(plot_funcs, rows, cols, figsize=None):
    """
    Arrange multiple plots in a grid.

    plot_funcs: list of callables, each taking an ax parameter.
                Each function should call one of the plot functions above
                with the ax= parameter, e.g.:
                  lambda ax: cayley_graph(6, 1, ax=ax)

    Returns the Figure.
    """
    if figsize is None:
        figsize = (4 * cols, 4 * rows)

    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    if rows == 1 and cols == 1:
        axes = np.array([axes])
    axes = np.atleast_2d(axes)

    for idx, func in enumerate(plot_funcs):
        r, c = divmod(idx, cols)
        if r < rows and c < cols:
            func(axes[r, c])

    # Hide unused axes
    for idx in range(len(plot_funcs), rows * cols):
        r, c = divmod(idx, cols)
        axes[r, c].axis('off')

    plt.tight_layout()
    plt.show()
    return fig
