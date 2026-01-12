rm -rf dist/
rm -rf build/
rm -rf __pycache__/
rm -rf .venv/

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install pyinstaller

pyinstaller Fleet-Command.spec