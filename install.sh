# Install dependencies and set up virtual environment for the game

rm -rf dist/
rm -rf build/
rm -rf __pycache__/
rm -rf .venv/

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt # Requirements for the game to be played

# Requirements for code formatting and compiling
pip install autopep8
pip install black
pip install pyinstaller