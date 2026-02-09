#!/usr/bin/env python3
"""Replace Python stdlib calls with SageMath equivalents in Jupyter notebooks.

Targets:
1. import time + time.time() -> walltime()
2. import random + random.randint(a,b) -> randint(a,b)
3. random.shuffle(L) -> shuffle(L) [available in SageMath]
4. random.sample(L, k) -> sample(L, k) [available in SageMath]
5. random.choice(L) -> L[randint(0, len(L)-1)]
6. import math + math.X() -> X() for known builtins
7. from itertools import combinations -> Combinations (SageMath)
8. from itertools import product -> (keep, no clean SageMath equiv)
9. import numpy as np -> remove (plots already converted)
"""

import json
import re
import sys
from pathlib import Path


# Track what we need from sage.misc.prandom per cell
PRANDOM_FUNCS = {'shuffle', 'sample', 'choice'}

# math.X -> SageMath equivalent
MATH_REPLACEMENTS = {
    'math.sqrt': 'sqrt',
    'math.log2': 'log2',
    'math.log': 'log',
    'math.ceil': 'ceil',
    'math.floor': 'floor',
    'math.pi': 'pi',
    'math.e': 'e',
    'math.gcd': 'gcd',
    'math.factorial': 'factorial',
    'math.isqrt': 'isqrt',
    'math.inf': 'Infinity',
}


def clean_cell_source(source_lines: list[str]) -> tuple[list[str], int]:
    """Clean Python imports in a single cell's source lines.

    Returns (cleaned_lines, fix_count).
    """
    fixes = 0
    cleaned = []

    # First pass: figure out what random functions are used (beyond randint)
    full_source = ''.join(source_lines)
    needs_prandom = set()
    if 'random.shuffle(' in full_source:
        needs_prandom.add('shuffle')
    if 'random.sample(' in full_source:
        needs_prandom.add('sample')

    for line in source_lines:
        original = line

        # --- import time ---
        if re.match(r'^import time\s*\\?\n?$', line.strip() if not line.endswith('\n') else line.rstrip('\n').strip()):
            stripped = line.strip().rstrip('\\').rstrip()
            if stripped == 'import time':
                fixes += 1
                continue  # remove the line

        # --- import random ---
        stripped_clean = line.strip().rstrip('\n')
        if stripped_clean == 'import random':
            if needs_prandom:
                # Replace with sage.misc.prandom import
                indent = line[:len(line) - len(line.lstrip())]
                funcs = ', '.join(sorted(needs_prandom))
                line = f'{indent}from sage.misc.prandom import {funcs}\n'
                fixes += 1
                cleaned.append(line)
                continue
            else:
                fixes += 1
                continue  # just remove it

        # --- import math ---
        if stripped_clean == 'import math':
            fixes += 1
            continue  # remove

        # --- import numpy as np ---
        if stripped_clean == 'import numpy as np' or stripped_clean == 'import numpy':
            fixes += 1
            continue  # remove

        # --- from itertools import combinations ---
        m = re.match(r'^(\s*)from itertools import combinations\s*$', stripped_clean)
        if m:
            fixes += 1
            continue  # remove, Combinations is a SageMath builtin

        # --- from collections import Counter ---
        # Keep this, no good SageMath equivalent

        # --- from collections import defaultdict ---
        # Keep this too

        # --- time.time() replacements ---
        if 'time.time()' in line:
            # Pattern: start = time.time()  ->  start = walltime()
            line = line.replace('time.time()', 'walltime()')
            if line != original:
                fixes += 1

        # --- random.randint(a, b) -> randint(a, b) ---
        if 'random.randint(' in line:
            line = line.replace('random.randint(', 'randint(')
            if line != original:
                fixes += 1
                original = line

        # --- random.shuffle(L) -> shuffle(L) ---
        if 'random.shuffle(' in line:
            line = line.replace('random.shuffle(', 'shuffle(')
            if line != original:
                fixes += 1
                original = line

        # --- random.sample(L, k) -> sample(L, k) ---
        if 'random.sample(' in line:
            line = line.replace('random.sample(', 'sample(')
            if line != original:
                fixes += 1
                original = line

        # --- random.choice(L) -> not replaced, rare ---
        # (would need complex parsing to replace cleanly)

        # --- math.X() -> X() ---
        for py_func, sage_func in MATH_REPLACEMENTS.items():
            if py_func in line:
                # Be careful with math.log2 vs math.log
                # Replace longer patterns first (already ordered in dict with log2 before log)
                line = line.replace(py_func, sage_func)

        if line != original:
            fixes += 1
            original = line

        # --- combinations( -> Combinations( ---
        # Only replace if we removed the itertools import in this cell
        if 'from itertools import combinations' in full_source:
            if 'combinations(' in line and 'Combinations(' not in line:
                # Don't replace inside strings or comments
                line = re.sub(r'\bcombinations\(', 'Combinations(', line)
                if line != original:
                    fixes += 1
                    original = line

        cleaned.append(line)

    return cleaned, fixes


def process_notebook(path: Path, dry_run: bool = False) -> int:
    """Process a single notebook. Returns number of fixes."""
    with open(path) as f:
        nb = json.load(f)

    total_fixes = 0
    modified = False

    for cell in nb.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue

        source = cell.get('source', [])
        if not source:
            continue

        cleaned, fixes = clean_cell_source(source)
        if fixes > 0:
            total_fixes += fixes
            if not dry_run:
                cell['source'] = cleaned
                modified = True

    if modified and not dry_run:
        with open(path, 'w') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write('\n')

    return total_fixes


def main():
    dry_run = '--dry-run' in sys.argv
    repo = Path(__file__).parent.parent

    notebooks = sorted(repo.glob('**/*.ipynb'))
    notebooks = [nb for nb in notebooks if '.ipynb_checkpoints' not in str(nb)]

    total = 0
    changed_files = 0

    for nb_path in notebooks:
        fixes = process_notebook(nb_path, dry_run=dry_run)
        if fixes > 0:
            rel = nb_path.relative_to(repo)
            print(f'  {rel}: {fixes} fixes')
            total += fixes
            changed_files += 1

    mode = 'DRY RUN' if dry_run else 'APPLIED'
    print(f'\n{mode}: {total} fixes across {changed_files} files')


if __name__ == '__main__':
    main()
