'''
The BM logic module. Bot process creation, and commencement of the match takes
place here.
'''
from sys import argv
from process import Process
import validate as const
from validate import validate, terminate, EndGameError, init, log

if len(argv) < 5:
    exit(0)

# inSB.py calls BM with bot extensions and a flag
# if flag==True swap players.
ext1, ext2, logfilename_suffix, swap = argv[1:5]
init(logfilename_suffix)

try:
    player1 = Process(ext1, "player1")
except Exception as e:
    log(valid=False, loser=1, cause="Unable to start bot")
    terminate(fail=True)

try:
    player2 = Process(ext2, "player2")
except Exception as e:
    log(loser=2, cause="Unable to start bot")
    terminate(bots=(player1, player1), fail=True)

if swap == "True":
    (player1, player2) = (player2, player1)
player = [player1, player2]

if player[0].is_alive():
    player[0].pass_input(const.P1)
else:
    log(valid=False, loser=1, cause="Premature termination")
    terminate(bots=player, loser=1)

if player[1].is_alive():
    player[1].pass_input(const.P2)
else:
    log(valid=False, loser=2, cause="Premature termination")
    terminate(bots=player, loser=2)

try:
    for i in range(2*const.ITER_MAX):
        if player[i%2].is_alive():
            actual_op = player[i%2].read_output()
            if actual_op is not None:
                player[i%2].suspend()
                player[(i+1)%2].resume()
                flipped_op = validate(actual_op)
                player[(i+1)%2].pass_input(flipped_op)
                if i%2 == 0:
                    log(valid=True, turn=const.P1, move=actual_op)
                else:
                    log(valid=True, turn=const.P2, move=flipped_op)
            else:
                log(valid=False, loser=(i%2)+1, cause='No IO detected')
                terminate(bots=player, loser=(i%2)+1)     # TLE
        else:
            # Premature Termination.
            log(valid=False, loser=(i%2)+1, cause="Premature termination")
            terminate(bots=player, loser=(i%2)+1)
    # Match did not terminate, DRAW
    log(valid=False, loser=-1, cause="Match did not terminate")
    terminate(bots=player, fail=True)
except IOError as ioe:
    log(valid=False, loser=(i%2)+1, cause=str(ioe))   # Unable to read output
    terminate(bots=player, loser=(i%2)+1)
except EndGameError as ege:
    # Logging handled in the validation
    terminate(bots=player, winner=ege.winner, draw=ege.draw)
except ValueError as ve:
    log(loser=(i%2)+1, move=actual_op.rstrip(), cause=str(ve))
    terminate(bots=player, loser=(i%2)+1)
