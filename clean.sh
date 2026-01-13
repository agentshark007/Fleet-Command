# Clean the code

rm -rf dist/
rm -rf build/
rm -rf __pycache__/

autopep8 --in-place --recursive .
black .

rm -rf __pycache__/