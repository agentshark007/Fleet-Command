import subprocess
import sys

PIPELINE = [
    ("autopep8", ["autopep8", "--in-place", "--recursive", "."]),
    ("ruff", [sys.executable, "-m", "ruff", "format", "."]),
    ("black", ["black", "."]),
]


def run():
    for name, cmd in PIPELINE:
        print(f"Running {name}...")
        try:
            subprocess.run(cmd, check=True)
            print(f"{name} completed successfully.\n")
        except subprocess.CalledProcessError:
            print(f"{name} failed.\n")


if __name__ == "__main__":
    run()
