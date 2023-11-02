import json
from tqdm import tqdm

def Pipeline(input_path, output_path, input_proto, output_proto, process,
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
        jin = input_proto(jobj)
        res = process(jin)
        if output_proto:
            output_proto(jobj, res)
        if output_file:
            output_file.write(json.dumps(jobj) + '\n')