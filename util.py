def is_comment(line: str) -> bool:
    return line.strip().startswith('#')

def replace_variables(variable_set: set, line: str):
    og = line
    for var in variable_set:
        line = line.replace(f'${var}', "f'{{}}'".replace("{}", var))
        # print("replaced", line)
    return line, og!=line

def try_split_in_two(l, s):
    # print(l)
    if not s in l:
        print(f"You most likely are missing a '{s}' somewhere:")
        print("Error occured here:")
        print(l)
        exit(1)
    try:
        l = l.split(s)
        return l[0], l[1]
    except:
        print(f"You most likely are missing a '{s}' somewhere:")
        print("Error occured here:")
        print(l)
        exit(1)

def r_until(s: str, b: str):
    return s[:s.find(b)][len(b):]
def r_from(s: str, b: str):
    return s[s.find(b):][len(b):]
def low_opts(l: list[list[str]]) -> list[list[str]]:
    return list(map(lambda x: list(map(lambda y: y.lower(), x)), l))
