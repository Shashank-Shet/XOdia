from Process import Process
from Validate import validate, terminate
from sys import argv

ext1, ext2, swap = argv[1:]

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

player = (player1, player2)
actual_and_flipped = [ "", "" ]

if player[0].isAlive():
    player[0].passInput(b'0')
else:
    terminate()
    
if player[1].isAlive():
    player[1].passInput(b'1')
else:
    terminate()

try:
    for i in range(50):
        if player[i%2].isAlive():
            actual_op = player[i%2].readOutput()
            if actual_op:
                flipped_op = validate(actual_op)
                player[(i+1)%2].passInput(flipped_op)
            else:
                terminate()           # TLE
        else:
            terminate()               # Premature Termination.
    else:
        terminate()                   # Match did not terminate, DRAW
except IOError as ioe:
    pass                              # Unable to read output
except EndGameError as ege:
    pass
