#!/usr/bin/env python3
"""Generate README showcase images using matplotlib (no SageMath needed)."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "images"
OUT.mkdir(parents=True, exist_ok=True)

# Consistent style
plt.rcParams.update({
    'figure.facecolor': '#0d1117',
    'axes.facecolor': '#0d1117',
    'text.color': '#e6edf3',
    'axes.labelcolor': '#e6edf3',
    'xtick.color': '#8b949e',
    'ytick.color': '#8b949e',
    'axes.edgecolor': '#30363d',
    'grid.color': '#21262d',
    'font.family': 'monospace',
})

CYAN = '#58a6ff'
GREEN = '#3fb950'
ORANGE = '#d29922'
RED = '#f85149'
PURPLE = '#bc8cff'
PINK = '#f778ba'


def generate_elliptic_curve():
    """Elliptic curve y^2 = x^3 - x + 1 with point addition."""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Curve
    x = np.linspace(-1.5, 2.5, 2000)
    rhs = x**3 - x + 1
    mask = rhs >= 0
    y = np.sqrt(np.maximum(rhs, 0))
    ax.plot(x[mask], y[mask], color=CYAN, linewidth=2.5)
    ax.plot(x[mask], -y[mask], color=CYAN, linewidth=2.5)

    # Two points P and Q on the curve
    px, py = 0.0, 1.0          # P: y^2 = 0 - 0 + 1 = 1
    qx, qy = 1.0, 1.0          # Q: y^2 = 1 - 1 + 1 = 1

    # Line through P and Q (slope = 0 since py == qy)
    m = (qy - py) / (qx - px) if qx != px else None
    if m is not None:
        # Third intersection: x^3 - x + 1 - (m*(x - px) + py)^2 = 0
        # For m=0, b=1: x^3 - x + 1 - 1 = x^3 - x = x(x-1)(x+1)
        # Roots: x = -1, 0, 1. Third root is x = -1
        rx = -1.0
        ry = m * (rx - px) + py  # = 1.0
        sx, sy = rx, -ry          # Reflect: P + Q = (rx, -ry) = (-1, -1)

    # Draw the secant line
    x_line = np.linspace(-1.8, 1.8, 100)
    y_line = m * (x_line - px) + py
    ax.plot(x_line, y_line, '--', color=ORANGE, linewidth=1.2, alpha=0.7)

    # Vertical reflection line
    ax.plot([rx, rx], [ry, sy], ':', color='#8b949e', linewidth=1.2, alpha=0.6)

    # Points
    ax.plot(px, py, 'o', color=GREEN, markersize=12, zorder=5)
    ax.annotate('P', (px, py), textcoords='offset points', xytext=(-15, 10),
                fontsize=14, fontweight='bold', color=GREEN)

    ax.plot(qx, qy, 'o', color=GREEN, markersize=12, zorder=5)
    ax.annotate('Q', (qx, qy), textcoords='offset points', xytext=(10, 10),
                fontsize=14, fontweight='bold', color=GREEN)

    ax.plot(rx, ry, 's', color=PURPLE, markersize=10, zorder=5, alpha=0.6)
    ax.annotate('R', (rx, ry), textcoords='offset points', xytext=(-18, 8),
                fontsize=12, color=PURPLE, alpha=0.7)

    ax.plot(sx, sy, '*', color=PINK, markersize=18, zorder=5)
    ax.annotate('P + Q', (sx, sy), textcoords='offset points', xytext=(10, -15),
                fontsize=14, fontweight='bold', color=PINK)

    ax.set_xlim(-2, 2.8)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title('Elliptic Curve Point Addition', fontsize=16, pad=15, color='#e6edf3')
    ax.set_xlabel('$x$', fontsize=13)
    ax.set_ylabel('$y$', fontsize=13)

    # Equation label
    ax.text(1.8, -2.4, r'$y^2 = x^3 - x + 1$', fontsize=13, color=CYAN,
            style='italic', ha='center')

    fig.tight_layout()
    fig.savefig(OUT / 'elliptic-curve.png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved {OUT / 'elliptic-curve.png'}")


def generate_lattice():
    """2D lattice with good vs bad basis."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

    # Good basis (short, nearly orthogonal)
    b1_good = np.array([2, 1])
    b2_good = np.array([0, 2])

    # Bad basis (long, nearly parallel)
    b1_bad = np.array([2, 5])
    b2_bad = np.array([4, 7])

    for ax, b1, b2, title, color in [
        (ax1, b1_good, b2_good, '"Good" Basis (Short, Orthogonal)', GREEN),
        (ax2, b1_bad, b2_bad, '"Bad" Basis (Long, Nearly Parallel)', RED),
    ]:
        # Generate lattice points
        pts = []
        for i in range(-4, 5):
            for j in range(-4, 5):
                p = i * b1 + j * b2
                if -10 <= p[0] <= 10 and -10 <= p[1] <= 10:
                    pts.append(p)

        pts = np.array(pts)
        ax.scatter(pts[:, 0], pts[:, 1], color=CYAN, s=30, zorder=4, alpha=0.8)

        # Basis vectors as arrows
        origin = np.array([0, 0])
        ax.annotate('', xy=b1, xytext=origin,
                     arrowprops=dict(arrowstyle='->', color=color, lw=2.5))
        ax.annotate('', xy=b2, xytext=origin,
                     arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2.5))

        ax.annotate(r'$\mathbf{b}_1$', xy=b1 / 2, textcoords='offset points',
                     xytext=(8, -12), fontsize=13, fontweight='bold', color=color)
        ax.annotate(r'$\mathbf{b}_2$', xy=b2 / 2, textcoords='offset points',
                     xytext=(-20, 5), fontsize=13, fontweight='bold', color=ORANGE)

        # Origin
        ax.plot(0, 0, 'o', color='white', markersize=8, zorder=5)

        ax.set_xlim(-8, 8)
        ax.set_ylim(-8, 8)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.2)
        ax.set_title(title, fontsize=12, pad=10, color='#e6edf3')

    fig.suptitle('Lattice Basis Reduction', fontsize=16, y=1.02, color='#e6edf3')
    fig.tight_layout()
    fig.savefig(OUT / 'lattice-basis.png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved {OUT / 'lattice-basis.png'}")


def generate_module_flow():
    """Visual diagram of the 4-phase learning flow."""
    fig, ax = plt.subplots(figsize=(12, 3.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.5)
    ax.axis('off')

    phases = [
        ('Explore', 'SageMath\nNotebooks', CYAN, 1.5),
        ('Implement', 'Rust\nExercises', GREEN, 4.5),
        ('Break', 'Attack Weak\nPrimitives', ORANGE, 7.5),
        ('Connect', 'Real-World\nProtocols', PURPLE, 10.5),
    ]

    box_w, box_h = 2.2, 2.2

    for name, subtitle, color, cx in phases:
        # Box
        rect = FancyBboxPatch((cx - box_w/2, 0.6), box_w, box_h,
                               boxstyle="round,pad=0.15",
                               facecolor=color + '18', edgecolor=color,
                               linewidth=2)
        ax.add_patch(rect)

        # Phase name
        ax.text(cx, 2.15, name, ha='center', va='center',
                fontsize=16, fontweight='bold', color=color)

        # Subtitle
        ax.text(cx, 1.35, subtitle, ha='center', va='center',
                fontsize=11, color='#8b949e')

    # Arrows between phases
    for i in range(3):
        x_start = phases[i][3] + box_w/2 + 0.05
        x_end = phases[i+1][3] - box_w/2 - 0.05
        ax.annotate('', xy=(x_end, 1.7), xytext=(x_start, 1.7),
                     arrowprops=dict(arrowstyle='->', color='#8b949e',
                                     lw=2, connectionstyle='arc3,rad=0'))

    # Stats bar at bottom
    ax.text(6, 0.15, '123 notebooks  |  57 Rust exercises  |  12 modules  |  BSc to postgrad',
            ha='center', va='center', fontsize=11, color='#8b949e', style='italic')

    fig.tight_layout()
    fig.savefig(OUT / 'module-flow.png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved {OUT / 'module-flow.png'}")


def generate_social_preview():
    """1280x640 social preview for GitHub link sharing."""
    fig, ax = plt.subplots(figsize=(12.8, 6.4))
    ax.set_xlim(0, 12.8)
    ax.set_ylim(0, 6.4)
    ax.axis('off')

    # Small elliptic curve in the bottom-right corner
    x = np.linspace(-1.2, 2.2, 1500)
    rhs = x**3 - x + 1
    mask = rhs >= 0
    y = np.sqrt(np.maximum(rhs, 0))
    # Scale and shift to bottom-right
    sx, sy_offset, scale = 9.5, 1.8, 0.9
    ax.plot(x[mask] * scale + sx, y[mask] * scale + sy_offset, color=CYAN, linewidth=1.8, alpha=0.35)
    ax.plot(x[mask] * scale + sx, -y[mask] * scale + sy_offset, color=CYAN, linewidth=1.8, alpha=0.35)

    # Title
    ax.text(6.4, 4.6, 'Crypto From First Principles', ha='center', va='center',
            fontsize=36, fontweight='bold', color='#e6edf3')

    # Stats line
    ax.text(6.4, 3.6, '123 notebooks  |  57 Rust exercises  |  12 modules',
            ha='center', va='center', fontsize=18, color=CYAN)

    # Tagline
    ax.text(6.4, 2.6, 'Learn the math. Build it in Rust. Break it. See it in the wild.',
            ha='center', va='center', fontsize=16, color='#8b949e', style='italic')

    # Phase chips at the bottom
    phases = [
        ('Explore', CYAN, 2.5),
        ('Implement', GREEN, 5.0),
        ('Break', ORANGE, 7.5),
        ('Connect', PURPLE, 10.0),
    ]
    for label, color, cx in phases:
        rect = FancyBboxPatch((cx - 1.0, 0.8), 2.0, 0.9,
                               boxstyle="round,pad=0.12",
                               facecolor=color + '20', edgecolor=color,
                               linewidth=1.5)
        ax.add_patch(rect)
        ax.text(cx, 1.25, label, ha='center', va='center',
                fontsize=14, fontweight='bold', color=color)

    fig.tight_layout(pad=0)
    fig.savefig(OUT / 'social-preview.png', dpi=100, bbox_inches='tight',
                facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print(f"  Saved {OUT / 'social-preview.png'}")


if __name__ == '__main__':
    print("Generating README images...")
    generate_elliptic_curve()
    generate_lattice()
    generate_module_flow()
    generate_social_preview()
    print("Done!")
