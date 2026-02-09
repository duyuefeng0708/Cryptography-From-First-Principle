#!/usr/bin/env python3
"""Fix corrupted notebook cells where source is stored as individual characters.

Some cells have source = ['#', ' ', 'c', 'o', 'm', 'p', 'u', 't', 'e', '\n', ...]
instead of source = ['# compute\n', ...]. This script joins the characters back
into proper line-delimited arrays.
"""

import json
import sys
from pathlib import Path


def is_char_corrupted(source: list[str]) -> bool:
    """Check if source is stored as individual characters."""
    if len(source) <= 10:
        return False
    single_chars = sum(1 for s in source if len(s) <= 2)
    return single_chars / len(source) > 0.8


def fix_source(source: list[str]) -> list[str]:
    """Join character-level source back into lines."""
    full_text = ''.join(source)
    if not full_text:
        return source

    # Split into lines, preserving newlines
    lines = full_text.split('\n')
    # Re-add newlines to all lines except the last (if it's empty)
    result = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            result.append(line + '\n')
        elif line:  # last line, only add if non-empty
            result.append(line)

    return result


def process_notebook(path: Path, dry_run: bool = False) -> int:
    """Process a single notebook. Returns number of fixed cells."""
    with open(path) as f:
        nb = json.load(f)

    fixed = 0
    modified = False

    for cell in nb.get('cells', []):
        source = cell.get('source', [])
        if not source:
            continue

        if is_char_corrupted(source):
            new_source = fix_source(source)
            fixed += 1
            if not dry_run:
                cell['source'] = new_source
                modified = True

    if modified and not dry_run:
        with open(path, 'w') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write('\n')

    return fixed


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
            print(f'  {rel}: {fixes} cells fixed')
            total += fixes
            changed_files += 1

    mode = 'DRY RUN' if dry_run else 'APPLIED'
    print(f'\n{mode}: {total} cells fixed across {changed_files} files')


if __name__ == '__main__':
    main()
