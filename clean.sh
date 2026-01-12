rm -rf dist/
rm -rf build/

autopep8 --in-place --recursive .
black .

rm -rf __pycache__/