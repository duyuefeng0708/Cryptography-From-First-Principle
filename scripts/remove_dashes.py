#!/usr/bin/env python3
"""Replace ' -- ' (double-hyphen dashes) in notebook markdown cells and code comments.

Rules:
- In markdown cells: replace ' -- ' with '. ' or ', '
- In code cells: replace ' -- ' only in comments (lines starting with #) and strings
- Skip table separator lines
- Skip code fences
"""

import json
import re
from pathlib import Path


def fix_dashes_in_text(text: str) -> str:
    """Replace ' -- ' dashes in a line of text."""
    if re.match(r'^[\s|:-]+$', text):
        return text
    if text.strip().startswith('```'):
        return text

    def replacer(m):
        after = text[m.end():m.end() + 1] if m.end() < len(text) else ''
        if after and (after.isupper() or after == '"' or after == "'"):
            return '. '
        return ', '

    return re.sub(r' -- ', replacer, text)


def fix_dashes_in_code_line(line: str) -> str:
    """Replace ' -- ' in code comments and print strings only."""
    if ' -- ' not in line:
        return line

    # Comment lines (# ...)
    if line.lstrip().startswith('#'):
        return fix_dashes_in_text(line)

    # Inside print/string: replace within quoted portions
    # Match f-strings and regular strings containing ' -- '
    def fix_string(m):
        return fix_dashes_in_text(m.group(0))

    # Fix inside single-quoted strings
    line = re.sub(r"'[^']*? -- [^']*?'", fix_string, line)
    # Fix inside double-quoted strings
    line = re.sub(r'"[^"]*? -- [^"]*?"', fix_string, line)

    return line


def process_notebook(path: Path) -> int:
    with open(path) as f:
        nb = json.load(f)

    changes = 0
    for cell in nb.get('cells', []):
        cell_type = cell.get('cell_type', '')
        new_source = []
        for line in cell['source']:
            if cell_type == 'markdown':
                fixed = fix_dashes_in_text(line)
            elif cell_type == 'code':
                fixed = fix_dashes_in_code_line(line)
            else:
                fixed = line
            if fixed != line:
                changes += 1
            new_source.append(fixed)
        cell['source'] = new_source

    if changes > 0:
        with open(path, 'w') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write('\n')

    return changes


def main():
    root = Path(__file__).resolve().parent.parent
    total = 0
    files_changed = 0

    for nb_path in sorted(root.rglob('*.ipynb')):
        if '.ipynb_checkpoints' in str(nb_path):
            continue
        n = process_notebook(nb_path)
        if n > 0:
            rel = nb_path.relative_to(root)
            print(f"  {rel}: {n} fixes")
            total += n
            files_changed += 1

    print(f"\nTotal: {total} fixes across {files_changed} files")


if __name__ == '__main__':
    main()
