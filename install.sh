# Install dependencies and set up virtual environment for the game

# Delete build folders
rm -rf dist/
rm -rf build/

# Delete cache and log files
rm -rf __pycache__/
rm -rf fleet-command.log

# Delete virtual environment
rm -rf .venv/

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install game requirements
pip install -r requirements.txt

# Install development tools
pip install autopep8
pip install isort
pip install black
pip install pyinstaller