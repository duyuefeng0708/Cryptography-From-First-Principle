#!/usr/bin/env python3
"""
Convert SageMath notebooks to pure Python notebooks using cryptolab.

Reads .ipynb files from sage/ directories, applies mechanical translations,
and writes to python/ directories. Manual review is still needed for
visualization-heavy cells.
"""

import json
import re
import sys
import os


# Standard header cell for all Python notebooks
HEADER_SOURCE = [
    "# This notebook has two versions:\n",
    "#   Python (this file) -- runs in browser via JupyterLite, no install needed\n",
    "#   SageMath (../sage/) -- richer algebra system, needs local install or Codespaces\n",
    "#\n",
    "# Both versions cover the same material. Choose whichever works for you.\n",
    "\n",
    "import sys, os\n",
    "sys.path.insert(0, os.path.join('..', '..', '..', 'shared'))\n",
]


# Import lines added based on what the notebook uses
IMPORT_MAP = {
    'Mod(': 'from cryptolab import Mod',
    'Zmod(': 'from cryptolab import Zmod',
    'Integers(': 'from cryptolab import Integers',
    'gcd(': 'from cryptolab import gcd',
    'euler_phi(': 'from cryptolab import euler_phi',
    'factor(': 'from cryptolab import factor',
    'divisors(': 'from cryptolab import divisors',
    'is_prime(': 'from cryptolab import is_prime',
    'power_mod(': 'from cryptolab import power_mod',
    'inverse_mod(': 'from cryptolab import inverse_mod',
    'primitive_root(': 'from cryptolab import primitive_root',
    'discrete_log(': 'from cryptolab import discrete_log',
    'CRT(': 'from cryptolab import crt',
    'DiGraph(': 'from cryptolab.plot import cayley_graph',
    'Poset(': 'from cryptolab.plot import subgroup_lattice',
    'matrix_plot(': 'from cryptolab.plot import multiplication_heatmap',
    'Graphics(': 'from cryptolab.plot import cycle_diagram, coset_coloring',
    'graphics_array(': 'from cryptolab.plot import graphics_array',
}


def detect_imports(notebook):
    """Scan all code cells to determine which imports are needed."""
    all_code = ''
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            all_code += ''.join(cell['source'])

    imports = set()
    for trigger, import_line in IMPORT_MAP.items():
        if trigger in all_code:
            imports.add(import_line)

    # Group imports from cryptolab
    cryptolab_names = []
    plot_names = []
    other_imports = []

    for imp in sorted(imports):
        if imp.startswith('from cryptolab.plot'):
            names = imp.replace('from cryptolab.plot import ', '').split(', ')
            plot_names.extend(names)
        elif imp.startswith('from cryptolab'):
            names = imp.replace('from cryptolab import ', '').split(', ')
            cryptolab_names.extend(names)
        else:
            other_imports.append(imp)

    lines = []
    if cryptolab_names:
        names_str = ', '.join(sorted(set(cryptolab_names)))
        lines.append(f'from cryptolab import {names_str}\n')
    if plot_names:
        names_str = ', '.join(sorted(set(plot_names)))
        lines.append(f'from cryptolab.plot import {names_str}\n')
    for imp in other_imports:
        lines.append(imp + '\n')

    return lines


def translate_code(source_lines):
    """Apply mechanical SageMath -> Python translations to code cell source."""
    result = []
    for line in source_lines:
        translated = translate_line(line)
        result.append(translated)
    return result


def translate_line(line):
    """Translate a single line of SageMath code to Python."""
    original = line

    # Remove SageMath-specific type conversions
    line = re.sub(r'\bInteger\(([^)]+)\)', r'int(\1)', line)
    line = re.sub(r'\bZZ\(([^)]+)\)', r'int(\1)', line)

    # CRT -> crt (lowercase)
    line = re.sub(r'\bCRT\(', 'crt(', line)

    # ^ -> ** for exponentiation (but not in strings or comments)
    # This is tricky - only translate ^ that are not in strings/comments
    line = translate_caret(line)

    # var('t') -> remove (not needed)
    if re.match(r"\s*var\s*\(\s*['\"]t['\"]\s*\)\s*$", line):
        return '# (SageMath variable declaration removed)\n'

    # SageMath math functions -> Python math
    line = re.sub(r'\bcos\(', 'math.cos(', line)
    line = re.sub(r'\bsin\(', 'math.sin(', line)
    line = re.sub(r'\bsqrt\(', 'math.sqrt(', line)
    line = re.sub(r'\babs\(', 'abs(', line)
    # pi -> math.pi (but not in strings)
    line = re.sub(r'\bpi\b(?![\'"])', 'math.pi', line)

    # If we added math references, we should note the import is needed
    # (handled by adding 'import math' in imports)

    return line


def translate_caret(line):
    """Replace ^ with ** outside of strings and comments."""
    # Skip if line is a comment
    stripped = line.lstrip()
    if stripped.startswith('#'):
        return line

    result = []
    in_string = False
    string_char = None
    i = 0
    while i < len(line):
        c = line[i]
        if in_string:
            result.append(c)
            if c == '\\' and i + 1 < len(line):
                result.append(line[i + 1])
                i += 2
                continue
            if c == string_char:
                in_string = False
            i += 1
        else:
            if c in ('"', "'"):
                # Check for triple quotes
                if line[i:i+3] in ('"""', "'''"):
                    result.append(line[i:i+3])
                    in_string = True
                    string_char = line[i:i+3]
                    i += 3
                    continue
                in_string = True
                string_char = c
                result.append(c)
                i += 1
            elif c == '#':
                # Rest of line is comment
                result.append(line[i:])
                break
            elif c == '^':
                result.append('**')
                i += 1
            else:
                result.append(c)
                i += 1
    return ''.join(result)


def needs_math_import(source_lines):
    """Check if any line uses math functions."""
    code = ''.join(source_lines)
    return any(f in code for f in ['math.cos', 'math.sin', 'math.sqrt', 'math.pi'])


def convert_notebook(input_path, output_path):
    """Convert a SageMath notebook to a Python notebook."""
    with open(input_path, 'r') as f:
        nb = json.load(f)

    # Detect needed imports
    import_lines = detect_imports(nb)

    # Check if math is needed after translation
    all_translated = []
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            translated = translate_code(cell['source'])
            all_translated.extend(translated)

    if needs_math_import(all_translated):
        import_lines.insert(0, 'import math\n')

    # Build header cell
    header_cell = {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': HEADER_SOURCE + ['\n'] + import_lines
    }

    # Convert cells
    new_cells = [header_cell]
    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            new_cell = {
                'cell_type': 'markdown',
                'metadata': {},
                'source': translate_markdown(cell['source'])
            }
            new_cells.append(new_cell)
        elif cell['cell_type'] == 'code':
            translated_source = translate_code(cell['source'])
            new_cell = {
                'cell_type': 'code',
                'execution_count': None,
                'metadata': {},
                'outputs': [],
                'source': translated_source
            }
            new_cells.append(new_cell)

    # Build output notebook with Python 3 kernel
    output_nb = {
        'nbformat': 4,
        'nbformat_minor': 5,
        'metadata': {
            'kernelspec': {
                'display_name': 'Python 3',
                'language': 'python',
                'name': 'python3'
            },
            'language_info': {
                'name': 'python',
                'version': '3.12.0'
            }
        },
        'cells': new_cells
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(output_nb, f, indent=1)

    return len(new_cells)


def translate_markdown(source_lines):
    """Translate markdown cells. Mostly verbatim but update SageMath references."""
    result = []
    for line in source_lines:
        # Update references to SageMath-specific tools
        line = line.replace("SageMath's `Mod()`", "`Mod()` from cryptolab")
        line = line.replace("SageMath's `Zmod(n)`", "`Zmod(n)` from cryptolab")
        line = line.replace('in SageMath', 'in Python')
        line = line.replace('SageMath computes this with', 'We can compute this with')
        line = line.replace('SageMath can also compute', 'We can also compute')
        line = line.replace('SageMath confirms:', 'Computed:')
        line = line.replace('Use `divmod()` and `Mod()` in SageMath',
                          'Use `divmod()` and `Mod()` from cryptolab')
        result.append(line)
    return result


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mod01 = os.path.join(base, 'foundations', '01-modular-arithmetic-groups')

    conversions = [
        ('sage/01a-integers-and-division.ipynb', 'python/01a-integers-and-division.ipynb'),
        ('sage/01b-modular-arithmetic.ipynb', 'python/01b-modular-arithmetic.ipynb'),
        ('sage/01c-groups-first-look.ipynb', 'python/01c-groups-first-look.ipynb'),
        ('sage/01d-cyclic-groups-generators.ipynb', 'python/01d-cyclic-groups-generators.ipynb'),
        ('sage/01e-subgroups-lagrange.ipynb', 'python/01e-subgroups-lagrange.ipynb'),
        ('sage/01f-group-visualization.ipynb', 'python/01f-group-visualization.ipynb'),
        ('break/weak-generator-attack.ipynb', 'python/break-weak-generator-attack.ipynb'),
        ('break/smooth-order-attack.ipynb', 'python/break-smooth-order-attack.ipynb'),
        ('connect/dh-parameter-selection.ipynb', 'python/connect-dh-parameter-selection.ipynb'),
        ('connect/rsa-key-generation.ipynb', 'python/connect-rsa-key-generation.ipynb'),
    ]

    for sage_rel, python_rel in conversions:
        sage_path = os.path.join(mod01, sage_rel)
        python_path = os.path.join(mod01, python_rel)
        if os.path.exists(sage_path):
            n_cells = convert_notebook(sage_path, python_path)
            print(f'  {sage_rel} -> {python_rel}  ({n_cells} cells)')
        else:
            print(f'  SKIP {sage_rel} (not found)')


if __name__ == '__main__':
    main()
