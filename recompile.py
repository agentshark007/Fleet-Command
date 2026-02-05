import ast
import os
import sys
from pathlib import Path

def reformat_file(path: Path):
    try:
        source = path.read_text(encoding='utf-8')
        tree = ast.parse(source)
        reformatted = ast.unparse(tree)
        path.write_text(reformatted + '\n', encoding='utf-8')
    except Exception as e:
        print(f'Skipped {path}: {e}')

def main():
    project_root = Path(__file__).resolve().parent
    rel_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    target = (project_root / rel_path).resolve()
    if target.is_file() and target.suffix == '.py':
        reformat_file(target)
        return
    if target.is_dir():
        for root, _, files in os.walk(target):
            if '.venv' in Path(root).parts:
                continue
            for name in files:
                if name.endswith('.py'):
                    reformat_file(Path(root) / name)
        return
    raise SystemExit('Invalid file or directory')
if __name__ == '__main__':
    main()
