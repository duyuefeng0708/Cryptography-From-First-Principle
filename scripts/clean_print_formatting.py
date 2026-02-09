#!/usr/bin/env python3
"""Clean up ugly ASCII-table formatting in Jupyter notebook code cells.

Targets:
1. Separator bars: print("=" * N) and print("-" * N) for N >= 20
2. Column-header lines: print(f"{'header':>N} | ...")
3. Excessive width specifiers: {:>N}, {:<N}, {:^N} for N >= 5
"""

import json
import re
import sys
from pathlib import Path


def is_separator_line(line: str) -> bool:
    """Check if a line is a pure separator bar like print("=" * 55)."""
    stripped = line.strip()
    # print("=" * 55) or print("-" * 55)
    if re.match(r'^print\(["\'][=\-]["\'] \* \d+\)$', stripped):
        n = int(re.search(r'\d+', stripped.split('*')[1]).group())
        return n >= 20
    return False


def is_column_header_line(line: str) -> bool:
    """Check if a line is a pure column header with alignment specs and pipes."""
    stripped = line.strip()
    # Lines like: print(f"{'p':>5} | {'|G|=p-1':>8} | ...")
    # Must have multiple | separators and alignment specs
    if not stripped.startswith('print(f"') and not stripped.startswith("print(f'"):
        return False
    # Count alignment specs and pipe separators
    align_specs = len(re.findall(r":\s*[><\^]\d+\}", stripped))
    pipes = stripped.count(' | ')
    # It's a header if it has 3+ alignment specs and 2+ pipes
    return align_specs >= 3 and pipes >= 2


def clean_width_specifiers(line: str) -> str:
    """Remove excessive width specifiers from f-string print lines.

    {:>8} -> {} for N >= 4
    {:>2} -> {:>2} (keep small padding for digit alignment)
    {val:>8} -> {val}
    """
    # Match f-string width specs like :>N}, :<N}, :^N} where N >= 4
    def replace_spec(m):
        prefix = m.group(1)  # everything before the colon
        width = int(m.group(3))
        suffix = m.group(4)  # closing brace
        if width >= 2:
            return prefix + suffix
        return m.group(0)  # keep :>1 etc (unlikely)

    # Pattern: {expr:>N} or {expr:<N} or {expr:^N}
    result = re.sub(r'(\{[^}]*?)(:[><\^])(\d+)(\})', replace_spec, line)
    return result


def clean_constant_fstrings(line: str) -> str:
    """Replace f"{'constant'}" patterns with just the constant in print lines.

    print(f'{"message"}  {"encrypted"}') -> print('message  encrypted')
    Only applies to print lines where ALL {} contain string literals.
    """
    if 'print(f' not in line:
        return line

    # Replace {"string_literal"} and {'string_literal'} with just the string
    # This pattern matches f-string expressions that are just quoted constants
    result = re.sub(r'\{"([^"{}]*)"\}', r'\1', line)
    result = re.sub(r"\{'([^'{}]*)'\}", r'\1', result)

    # If there are no remaining { } expressions, downgrade f-string to plain string
    # But only if no other { remain (besides the ones we replaced)
    if result != line:
        # Check if there are still f-string expressions
        # Find the print(f'...' or print(f"..." part
        match = re.match(r"(\s*print\(f)(['\"])(.*)\2\)(.*)$", result)
        if match:
            prefix, quote, body, suffix = match.groups()
            # If no { remain in body, downgrade to plain string
            if '{' not in body:
                result = f"{prefix[:-1]}{quote}{body}{quote}){suffix}"

    return result


def clean_str_concat_in_fstring(line: str) -> str:
    """Replace {"text" + str(var) + "text"} with text{var}text in f-strings.

    Example:
      f'{"a^" + str(p-1) + " mod " + str(p)}'  ->  f'a^{p-1} mod {p}'
    """
    if 'str(' not in line:
        return line

    # Pattern: {"literal" + str(expr) + "literal" ...}
    # This can chain: {"a" + str(x) + " b " + str(y) + "c"}
    # Strategy: find expressions like {"..." + str(...) + "..."} and simplify

    def simplify_concat(m):
        """Simplify a single {concat_expression}."""
        inner = m.group(1)

        # Split on ' + ' or " + " while respecting quotes
        # Simple approach: try to parse the concatenation
        parts = []
        remaining = inner.strip()

        while remaining:
            remaining = remaining.strip()
            if remaining.startswith('"'):
                # String literal with double quotes
                end = remaining.index('"', 1)
                parts.append(('str', remaining[1:end]))
                remaining = remaining[end+1:].strip()
                if remaining.startswith('+'):
                    remaining = remaining[1:].strip()
            elif remaining.startswith("'"):
                # String literal with single quotes
                end = remaining.index("'", 1)
                parts.append(('str', remaining[1:end]))
                remaining = remaining[end+1:].strip()
                if remaining.startswith('+'):
                    remaining = remaining[1:].strip()
            elif remaining.startswith('str('):
                # str(expr) call
                depth = 0
                i = 4  # skip 'str('
                depth = 1
                while i < len(remaining) and depth > 0:
                    if remaining[i] == '(':
                        depth += 1
                    elif remaining[i] == ')':
                        depth -= 1
                    i += 1
                expr = remaining[4:i-1]
                parts.append(('expr', expr))
                remaining = remaining[i:].strip()
                if remaining.startswith('+'):
                    remaining = remaining[1:].strip()
            else:
                # Can't parse, bail out
                return m.group(0)

        if not parts:
            return m.group(0)

        # Rebuild as plain text + {expr} sequences
        result = ''
        for kind, val in parts:
            if kind == 'str':
                result += val
            elif kind == 'expr':
                result += '{' + val + '}'

        return result

    # Find all {expression} blocks in f-strings that contain str() + concatenation
    result = re.sub(r'\{(".*?str\(.*?")\}', simplify_concat, line)
    result = re.sub(r"\{('.*?str\(.*?')\}", simplify_concat, result)

    return result


def clean_cell_source(source_lines: list[str]) -> tuple[list[str], int]:
    """Clean formatting in a single cell's source lines.

    Returns (cleaned_lines, fix_count).
    """
    fixes = 0
    cleaned = []

    for line in source_lines:
        # Remove separator bars
        if is_separator_line(line):
            fixes += 1
            continue

        # Remove pure column header lines
        if is_column_header_line(line):
            fixes += 1
            continue

        # Clean width specifiers in print lines
        new_line = clean_width_specifiers(line)
        if new_line != line:
            fixes += 1
            line = new_line

        # Clean constant f-string expressions like f"{'header'}"
        new_line = clean_constant_fstrings(line)
        if new_line != line:
            fixes += 1
            line = new_line

        # Clean string concatenation in f-strings: {"a" + str(x) + "b"} -> a{x}b
        new_line = clean_str_concat_in_fstring(line)
        if new_line != line:
            fixes += 1
            line = new_line

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
    # Skip checkpoints
    notebooks = [nb for nb in notebooks if '.ipynb_checkpoints' not in str(nb)]

    total = 0
    changed_files = 0

    for nb_path in notebooks:
        fixes = process_notebook(nb_path, dry_run=dry_run)
        if fixes > 0:
            rel = nb_path.relative_to(repo)
            print(f"  {rel}: {fixes} fixes")
            total += fixes
            changed_files += 1

    mode = "DRY RUN" if dry_run else "APPLIED"
    print(f"\n{mode}: {total} fixes across {changed_files} files")


if __name__ == '__main__':
    main()
