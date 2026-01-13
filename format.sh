# Formats the codebase using autopep8, isort, and black.

autopep8 --in-place --recursive --aggressive --aggressive .
isort .
black .
