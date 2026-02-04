# Install dependencies and set up virtual environment for the game

# Delete virtual environment
rm -rf .venv/

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt
