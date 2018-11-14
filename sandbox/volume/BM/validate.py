'''
This module handles the interfacing between validation and the BM.
It houses the conventions for:
    1.) Passing bot output to validation and back.
    2.) Handling termination criteria.
    3.) Log file generation.
    4.) Bot termination.
    5.) Bot representation convention. eg 1 for p1, and 0 for p2.
'''

from subprocess import Popen, PIPE
from __init__ import logdir

val_proc = None
logfilename = None
logs = []

# IMPORTANT CONSTANTS
ITER_MAX = 50
P1 = b'1'
P2 = b'0'
INCONCLUSIVE = 103
P1_WIN = 101
P2_WIN = 102
DRAW = 100

def init(logfilesuffix):
    '''
    Runs validation process, and sets filename to save logs to when the match
    terminates.
    '''
    global logfilename, val_proc
    val_proc = Popen(["stdbuf", "-i0", "-o0", "-e0", "./val"], stdin=PIPE, stdout=PIPE)
    logfilename = logdir + "log" + logfilesuffix

def validate(ip_string):
    '''
    Interface between bots and validation. Pass output from the bot to the
    validation. Validation first returns the nature of the move, as valid,
    invalid, or termination. Correspondingly it performs appropriate actions.
    '''
    ip_string = ip_string.rstrip() + b'\n'       # Enforce trailing newline
    val_proc.stdin.write(ip_string)
    val_proc.stdin.flush()
    status = val_proc.stdout.readline().rstrip()
    if status == b'VALID':
        return val_proc.stdout.readline().rstrip()
    if status == b'WIN':
        end_move = val_proc.stdout.readline().rstrip()
        who_won = val_proc.stdout.readline().rstrip()
        win_condn = val_proc.stdout.readline().rstrip()
        if who_won == P1:
            who_won = 1
        else:
            who_won = 2
        log(win_or_draw=True, move=end_move, cause=win_condn)
        raise EndGameError(winner=who_won)
    elif status == b'DRAW':
        end_move = val_proc.stdout.readline().rstrip()
        turn_string = val_proc.stdout.readline().rstrip()
        log(win_or_draw=False, move=end_move, turn=turn_string)
        raise EndGameError(draw=True)
    else:
        raise ValueError(status.decode())

def terminate(bots=None, loser=None, winner=None, draw=False, fail=False):
    '''
    Cleanup operations. The function terminates the bots (if necessary), the
    validation process, and writes the logs to the logfile. It terminates
    the BM returning the appropriate error code.

    Parameters:
    ----------

    bots: tuple
        A tuple of bot processes. Optional.

    '''
    if not bots:
        bots[0].kill()
        bots[1].kill()
    val_proc.kill()
    with open(logfilename, 'w') as f:
        for line in logs:
            f.write(line)
    if winner == 1:
        err_code = P1_WIN
    elif winner == 2:
        err_code = P2_WIN
    elif loser == 1:
        err_code = P2_WIN
    elif loser == 2:
        err_code = P1_WIN
    elif draw is True:
        err_code = DRAW
    elif fail is True:
        err_code = INCONCLUSIVE
    exit(err_code)

def log(valid=None, loser=None, cause=None, move=None, turn=None, win_or_draw=None):
    '''
    Defines the logging convention.

    Parameters:
    ----------

    valid: boolean
        If True move is valid, else move is invalid. If not passed, then
    the move was flagged as incorrect by validation.

    loser: int (1 or 2)
        The player number who lost. If this parameter is passed it is first
    converted to the representation by UI and validation. It either occurs with
    the valid parameter or standalone.

    win_or_draw: boolean
        If True, win condition has occurred. Else draw condition.

    cause: str
        Reason of loss. Passed along with loser parameter.

    move: str
        The actual move which caused the win/loss/draw. Passed along with the
    loser parameter or win_or_draw parameter.

    turn: str
        Represents whose move it was.
    '''
    # byte strings are used by the bots, but when used within f strings,
    # the token 'b' appears, violating the communication conventions,
    # Hence decode is used.
    if move:
        move = move.decode()
    if turn:
        turn = turn.decode()
    if cause and isinstance(cause, bytes):
        cause = cause.decode()

    if win_or_draw is True:
        logs.append(f'w,{move},{cause}\n')
        return
    if win_or_draw is False:
        logs.append(f'd,{move},{turn}\n')
        return

    if loser == 1:
        loser = P1.decode()
    elif loser == 2:
        loser = P2.decode()

    if valid is True:
        logs.append(f'v,{turn},{move}\n')
    elif valid is False:
        logs.append(f'i,{loser},{cause}\n')
    elif loser is not None:
        logs.append(f'l,{loser},{move},{cause}\n')


class EndGameError(Exception):
    '''
    Custom exception to signify endgame condition. Raised only if a player wins
    or the match is a draw. Also the necessary logging is completed beforehand
    so after the exception is raised, only termination is left.
    '''

    def __init__(self, winner=None, draw=False):
        '''
        Constructor with mutually exclusive parameters. When draw is True,
        winner is None. If draw is False, winner is 1 or 2.
        '''
        super(EndGameError, self).__init__()
        self.winner, self.draw = winner, draw
