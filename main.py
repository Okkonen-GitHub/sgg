import sys

from util import is_comment, low_opts, r_from, r_until, replace_variables, try_split_in_two
from conf import Config, parse_config

def gen_var(v: str, q: str, n: str) -> str:
    return f'{v}=input("{q}")\n{n}()\n'

def gen_sp(v: str) -> str:
    return f'print("{v}")\n'

def parse_opts(opts: str):
    popts = []
    opts = opts.split(',')
    for opt in opts:
        if '/' in opt:
            popts.append(list(map(lambda x: x.strip(), opt.split('/'))))
        else:
            popts.append(opt)
    return popts

def gen_evnt(n: str, p: str, opts: list[str], nxt: list[str], config: Config) -> str:
    print(opts)
    print(nxt)
    if not len(opts) == len(nxt):
        print("The amount of options does not match the amount of follow up events")
        print(f"Error occured at {n}")
        exit(1)
    nxt = str(nxt).replace("'", "")
    if config.case_sensitive:
        return f'''def {n}():
    o={opts}
    n=[{nxt}]
    a=""
    c = []
    for e in o:
        c+=e
    while not a in c:
        a=input("{p}")
    for i in range(len(o)):
        for d in o:
            if a==d[i]:
                n[i]()
'''

    else:
        opts=low_opts(opts)
        return f'''def {n}():
    o={opts}
    n={nxt}
    a=""
    c = []
    for e in o:
        c+=e
    while not a in c:
        a=input("{p}").lower()
    for i in range(len(o)):
        for d in o:
            if a==d[i]:
                n[i]()

'''


def parse(lines):
    gc = ""
    config, lines = parse_config(lines)
    variable_set: set = set()
    # print(lines)

    for line in lines:
        if not is_comment(line):
            line = line.replace("\n", "").strip()
            if len(line) == 0:
                continue # skip blank lines
            line = replace_variables(variable_set, line)
            # if variable is declared
            if line.startswith('$'):
                var, val = try_split_in_two(line, ':')
                var = var[1:] # remove the prefix ($)
                prompt = r_until(val, '-').strip()
                next = r_from(val, '> ').strip()
                variable_set.add(var)
                gc+=gen_var(var, prompt, next)
            # if a text prompt
            elif line.startswith('@'):
                # TODO improve
                var, val = try_split_in_two(line, ':')
                var = var[1:]
                gc+=gen_sp(val.strip())
            else:
                name, evnt = try_split_in_two(line, ':')
                evnt = evnt[:evnt.find('->')].strip()
                opts = r_from(line, '(').strip().split('->')[0].strip()[:-1]
                opts = parse_opts(opts)
                next = list(map(lambda x: x.strip(), r_from(r_from(line, '->').strip(), '(').replace(')', '').split(',')))
                print(gen_evnt(name,evnt,opts,next, config))
                

                
                       
        # else: print("skip")



    print(gc)


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        with open(args[0], 'r') as f:
            game_data = f.readlines()
    except FileNotFoundError:
        print("Error, must pass a file as input")
        exit(1)
    parse(game_data)
