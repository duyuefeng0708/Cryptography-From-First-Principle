"""Smoke tests for cryptolab.plot."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for testing

from cryptolab.plot import (
    cayley_graph, cycle_diagram, subgroup_lattice,
    multiplication_heatmap, coset_coloring, graphics_array,
)


def test_cayley_graph_returns_figure():
    fig = cayley_graph(6, 1, op='add', figsize=3)
    assert fig is not None

def test_cayley_graph_non_generator():
    fig = cayley_graph(6, 2, op='add', figsize=3)
    assert fig is not None

def test_cycle_diagram_returns_figure():
    elements = [1, 2, 3, 4, 5, 6]
    fig = cycle_diagram(7, elements, 3, op='mul', figsize=3)
    assert fig is not None

def test_subgroup_lattice_returns_figure():
    fig = subgroup_lattice(12, figsize=4)
    assert fig is not None

def test_multiplication_heatmap_returns_figure():
    table = [[0, 0, 0], [0, 1, 2], [0, 2, 1]]
    fig = multiplication_heatmap(table, labels=[0, 1, 2], figsize=3)
    assert fig is not None

def test_coset_coloring_returns_figure():
    fig = coset_coloring(12, [0, 4, 8], figsize=3)
    assert fig is not None

def test_graphics_array_returns_figure():
    funcs = [
        lambda ax: cayley_graph(6, 1, op='add', ax=ax),
        lambda ax: cayley_graph(6, 2, op='add', ax=ax),
    ]
    fig = graphics_array(funcs, 1, 2, figsize=(6, 3))
    assert fig is not None
