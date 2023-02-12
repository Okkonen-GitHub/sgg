import sys

from util import is_comment, low_opts, r_from, r_until, replace_variables, try_split_in_two
from conf import Config, parse_config

def gen_var(v: str, q: str, n: str, prev, vars: set) -> str:
    i = f"{vars}".replace("'", "").replace('{','').replace('}','') if len(vars) != 0 else ''
    return f'''def {v}({i}):
    {prev}({i})
    {v}=input(f"{q} ")
    {n}({v})\n
'''

def gen_sp(name: str, v: str, vars: set) -> str:
    i = f"{vars}".replace("'", "").replace('{','').replace('}','') if len(vars) != 0 else ''
    return f'''def {name}({i}):
    print(f"{v}")\n
'''

def parse_opts(opts: str) -> list[list[str]]:
    popts = []
    opts = opts.split(',')
    for opt in opts:
        if '/' in opt:
            popts.append(list(map(lambda x: x.strip(), opt.split('/'))))
        else:
            popts.append(opt)
    return popts

def gen_evnt(n: str, p: str, prev: str, opts: list[list[str]], nxt: list[str], config: Config, replaced: bool, vars: set) -> str:
    # print(opts)
    # print(nxt)
    i = f"{vars}".replace("'", "").replace('{','').replace('}','') if len(vars) != 0 else ''
    if not len(opts) == len(nxt):
        print("The amount of options does not match the amount of follow up events")
        print(f"Error occured at {n}")
        exit(1)
    nxt = str(nxt).replace("'", "")
    if config.case_sensitive:
        return f'''def {n}({i}):
    {prev}({i})
    o={opts}
    n=[{nxt}]
    a=""
    c = []
    for e in o:
        c+=e
    while not a in c:
        a=input(f"{p} ")
    for i in range(len(o)):
        for d in o[i]:
            if a==d:
                n[i]({i})
'''

    else:
        opts=low_opts(opts)
        return f'''def {n}({i}):
    {prev}({i})
    o={opts}
    n={nxt}
    a=""
    c = []
    for e in o:
        c+=e
    while not a in c:
        a=input(f"{p} ").lower()
    for i in range(len(o)):
        for d in o[i]:
            if a==d:
                n[i]({i})

'''


def parse(lines: list[str]):
    gc = ""
    sl = ""
    config, lines = parse_config(lines)
    variable_set: set = set()
    # print(lines)
    is_empty = lambda l: len(l)!=0
    remove_whitespace = lambda l: l.replace('\n', '').strip()
    remove_comments = lambda l: not is_comment(l)
    lines = list(
            filter(remove_comments,
            filter(is_empty,
            map(remove_whitespace, lines)
        ))
    )
    for line in lines:
        if not is_comment(line):

            nline, replaced = replace_variables(variable_set, line)
            # if variable is declared
            if nline.startswith('$'):
                info = lines[lines.index(line)-1]
                if info.startswith('@'):
                    info, _ = parse([info])
                    iname = info.split(' ')[1][:-4]
                else:
                    iname = '#'

                var, val = try_split_in_two(nline, ':')
                var = var[1:] # remove the prefix ($)
                prompt = r_until(val, '-').strip()
                next = r_from(val, '> ').strip()
                gc+=gen_var(var, prompt, next, iname, variable_set)
                variable_set.add(var)
            # if a text prompt
            elif nline.startswith('@'):
                var, val = try_split_in_two(nline, ':')
                var = var[1:]
                # print(lines)
                gc+=gen_sp(var.strip(), val.strip(), variable_set)
            # the starting logic
            elif nline.startswith('!'):
                start, vars = parse([nline[1:]])
                variable_set=variable_set.union(vars)
                gc+=start
                sl+=start.split(' ')[1][:-2]
            # a normal event
            else:
                info = lines[lines.index(line)-1]
                if info.startswith('@'):
                    info, _ = parse([info])
                    iname = info.split(' ')[1][:-4]
                else:
                    iname = '#'

                name, evnt = try_split_in_two(nline, ':')
                evnt = evnt[:evnt.find('->')].strip()
                opts = r_from(nline, '(').strip().split('->')[0].strip()[:-1]
                opts = parse_opts(opts)
                next = list(map(lambda x: x.strip(), r_from(r_from(nline, '->').strip(), '(').replace(')', '').split(',')))
                gc+=gen_evnt(name,evnt, iname,opts,next, config, replaced, variable_set)
                

                
    return gc+sl, variable_set


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        with open(args[0], 'r') as f:
            game_data = f.readlines()
    except FileNotFoundError:
        print("Error, must pass a file as input")
        exit(1)
    code, _ = parse(game_data)
    print(code)
