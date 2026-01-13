# Clean the code

rm -rf build/
rm -rf __pycache__/
rm -rf fleet-command.log

autopep8 --in-place --recursive .
black .

rm -rf __pycache__/