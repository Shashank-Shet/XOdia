from subprocess import call

val_proc = None

def validate(ip_string):
    ip_string = ip_string.rstrip('\n') + '\n'
    val_proc.stdin.write(ip_string)
    status = val_proc.stdout.readline().rstrip('\n')
    if bucket == 'VALID':
        return val_proc.stdout.readline()
    elif bucket == 'WIN':
        pass
    elif bucket = 'DRAW':
        pass
    else:
        pass

def terminate(**kwargs):
    if kwargs.get("loser"):
        pass
    elif kwargs.get("winner"):
        pass
    else:
        
    pass

class EndGameError(Exception):
    pass

def log(s):
    pass   
