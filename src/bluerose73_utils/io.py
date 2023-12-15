import os
import argparse
import json
import warnings

def IOParser(**kwargs):
    parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    return parser

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

def ReadJsonLines(*paths):
    '''
    Joins paths to make the full filename.
    Then read and parse the JSON Lines file into a list.
    '''
    with open(os.path.join(*paths)) as f:
        return [json.loads(line) for line in f]

class Workspace:
    '''
    A workspace saves json or jsonlines objects in a dedicated folder.

    Offers a simple interface for closely co-operating programs to
    use each other's results.
    '''

    def __init__(self, path: str = None, list_format: str = 'jsonl'):
        '''
        Parameters
        ----------
        path: str
            Root path of this workspace. If not specified, use cli argument --workspace
        list_format: str
            'json' or 'jsonl'. If the object is a list, whether to store it as json list or as jsonlines.
        '''
        if path is None:
            parser = argparse.ArgumentParser()
            parser.add_argument('-w', '--workspace', required=True)
            args = parser.parse_args()
            path = args.workspace
        self.root_path = path
        self.list_format = list_format
        os.makedirs(path, exist_ok=True)

    def save(self, obj, name: str):
        if isinstance(obj, list) and self.list_format == 'jsonl':
            with open(os.path.join(self.root_path, name + '.jsonl'), 'w') as f:
                for line in obj:
                    f.write(json.dumps(line) + '\n')
        else:
            with open(os.path.join(self.root_path, name + '.json'), 'w') as f:
                json.dump(obj, f)
                

    def load(self, name: str):
        file_list = os.listdir(self.root_path)
        target_filename = None
        for filename in file_list:
            if name + '.json' == filename or name + '.jsonl' == filename:
                if target_filename is not None:
                    warnings.warn(f'Found more than one files with name {name}, using {target_filename}')
                else:
                    target_filename = filename
        if target_filename is None:
            raise FileNotFoundError(name)
        if target_filename.endswith('.jsonl'):
            return [json.loads(line) for line in ReadLines(self.root_path, target_filename)]
        else:
            return json.loads(ReadFile(self.root_path, target_filename))

    def loadtext(self, name: str):
        return ReadFile(self.root_path, name)