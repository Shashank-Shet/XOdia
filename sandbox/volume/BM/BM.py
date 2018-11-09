from sys import argv
from process import Process
from Validate import validate, terminate, EndGameError, log

# inSB.py calls BM with bot extensions and a flag
# if flag==True swap players.
ext1, ext2, swap = argv[1:4]

try:
    player1 = Process(ext1, "player1")
except Exception as e:
    terminate()

try:
    player2 = Process(ext2, "player2")
except Exception as e:
    terminate()

if swap == "True":
    (player1, player2) = (player2, player1)

player = [player1, player2]

if player[0].is_alive():
    player[0].pass_input(b'0')
else:
    terminate(loser=1)

if player[1].is_alive():
    player[1].pass_input(b'1')
else:
    terminate(loser=2)

try:
    for i in range(50):
        if player[i%2].is_alive():
            actual_op = player[i%2].read_output()
            if actual_op is not None:
                flipped_op = validate(actual_op)
                player[(i+1)%2].pass_input(flipped_op)
                if i%2 == 0:
                    log(actual_op)
                else:
                    log(flipped_op)
            else:
                terminate(loser=(i%2)+1)     # TLE
        else:
            terminate(loser=(i%2)+1)         # Premature Termination.
    terminate(draw=True)                     # Match did not terminate, DRAW
except IOError as ioe:
    terminate(loser=(i%2)+1)                 # Unable to read output
except EndGameError as ege:
    terminate()
