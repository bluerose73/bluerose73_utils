import json
from tqdm import tqdm
import warnings
warnings.warn("This module is deprecated.", DeprecationWarning,
              stacklevel=2)

def Pipeline(input_path, output_path, process, input_proto=None, output_proto=None,
                  max_lines=-1):
    input_file = open(input_path)
    if output_path:
        output_file = open(output_path, 'w')
    else:
        output_file = None
    for line_id, line in enumerate(tqdm(input_file, desc=input_path)):
        if max_lines >= 0 and line_id >= max_lines:
            break
        jobj = json.loads(line)
        if input_proto:
            jin = input_proto(jobj)
        else:
            jin = jobj
        res = process(jin)
        if output_proto:
            output_proto(jobj, res)
        if output_file:
            output_file.write(json.dumps(jobj) + '\n')