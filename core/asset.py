import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def asset(path):
    return os.path.join(BASE_PATH, '../assets', path)
