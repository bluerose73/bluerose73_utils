import textwrap

def Wrap(body: str):
    return '\n'.join(['\n'.join(textwrap.wrap(line, 90,
                     break_long_words=False, replace_whitespace=False))
                     for line in body.splitlines() if line.strip() != ''])
