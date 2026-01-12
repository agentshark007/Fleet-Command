rm -rf build/

autopep8 --in-place --recursive .
ruff -w .
black .

rm -rf __pycache__/