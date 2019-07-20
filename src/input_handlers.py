from blessed.keyboard import Keystroke

def handle_keys(inp: Keystroke):
    if inp in 'q' or inp.name == 'KEY_ESCAPE':
        return {'exit': True}

    if inp in 'wk':
        return {'move': (0,-1)}
    elif inp in 'sj':
        return {'move': (0,1)}
    elif inp in 'ah':
        return {'move': (-1,0)}
    elif inp in 'dl':
        return {'move': (1,0)}
    else:
        return {'no_op': True}
