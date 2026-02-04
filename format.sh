# Delete build artifacts and format the codebase

echo "Deleting build artifacts..."
rm -rf build/
rm -rf dist/
echo "Build artifacts deleted."

echo "Deleting __pycache__ directories..."
rm -rf __pycache__/
echo "__pycache__ directories deleted."

echo "Deleting log files..."
rm -rf fleet-command.log
echo "Log files deleted."

echo "Formatting codebase..."
python recompile.py ""
autopep8 --in-place --recursive --aggressive --aggressive .
isort .
black .
echo "Codebase formatted."
