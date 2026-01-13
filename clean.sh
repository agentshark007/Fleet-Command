# Removes build artifacts and formats Python code in the current directory and its subdirectories.

rm -rf build/
rm -rf __pycache__/
rm -rf fleet-command.log

chmod +x format.sh
./format.sh
