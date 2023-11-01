import os

def ReadFile(*paths):
    '''
    Joins paths to make the full filename,
    and read the file into a single string.
    '''
    with open(os.path.join(*paths)) as f:
        return f.read()
    
def ReadLines(*paths):
    '''
    Joins paths to make the full filename,
    and read the file into a list of lines.
    '''
    with open(os.path.join(*paths)) as f:
        return f.readlines()
