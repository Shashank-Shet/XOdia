# run this code with follwing command line args
# argv[1] -> bot1 path (absolute)
# argv[2] -> bot2 path (absolute)
# argv[3] -> log file path (absolute)

from subprocess import call, Popen, PIPE
from select import poll, POLLIN
from signal import signal, alarm, SIGALRM
from sys import exit, argv
from val_parser import parser_func, EndGameError

selected_time_limits = {
    "cpp": 2000,
    "c": 2000,
    "py": 6000,
}

ext1 = argv[1]
ext2 = argv[2]

time_limit = [ selected_time_limits[ext1], selected_time_limits[ext2] ]

# 3rd list item will be replaced by PID of players' processes
plist1 = ["prlimit", "-p", ""]
plist2 = ["prlimit", "-p", ""]

log_file = open( '../matches/log' + argv[3] , 'w')

# NOTE: Compiling will not be done in the BM code in the final project.
# This is only here for convenience and testing
# call(["g++", "-o", "player1", "bot.cpp"])
# call(["g++", "-o", "player2", "bot.cpp"])
call(["g++", "-std=c++11", "-o", "val", "val.cpp"])

try:
    if ext1=="cpp":
        plist1.extend(("--nofile=5", "--nproc=500", "--as=21460"))
        player1_proc = Popen(["stdbuf", "-o0", "-i0", "-e0", "../bots/player1"], stdin=PIPE, stdout=PIPE)
    elif ext1=="c":
        plist1.extend(("--nofile=5", "--nproc=500", "--as=21460"))
        player1_proc = Popen(["stdbuf", "-o0", "-i0", "-e0", "../bots/player1"], stdin=PIPE, stdout=PIPE)
    else:
        plist1.extend(("--nofile=5", "--nproc=500", "--as=32740"))
        player1_proc = Popen(["stdbuf", "-o0", "-i0", "-e0", "python", "player1"], stdin=PIPE, stdout=PIPE)
except Exception as e:
    print "Error occured in process creation"
    end_code(-1)

try:
    if ext2=="cpp":
        plist2.extend(("--nofile=5", "--nproc=500", "--as=21460"))
        player2_proc = Popen(["stdbuf", "-o0", "-i0", "-e0", "../bots/player2"], stdin=PIPE, stdout=PIPE)
    elif ext2=="c":
        plist2.extend(("--nofile=5", "--nproc=500", "--as=21460"))
        player2_proc = Popen(["stdbuf", "-o0", "-i0", "-e0", "../bots/player2"], stdin=PIPE, stdout=PIPE)
    else:
        plist2.extend(("--nofile=5", "--nproc=500", "--as=32740"))
        player2_proc = Popen(["stdbuf", "-o0", "-i0", "-e0", "python", "../bots/player2"], stdin=PIPE, stdout=PIPE)
except Exception as e:
    print "Error occurred in process creation"
    end_code(-1)

popen_val_obj = Popen(["stdbuf", "-o0", "-i0", "-e0", "./val"], stdin=PIPE, stdout=PIPE)

plist1[2] = str(player1_proc.pid)
plist2[2] = str(player2_proc.pid)

player = [player1_proc, player2_proc]

# Run bots
call(plist1)
call(plist2)

if argv[4] == "True":               # Swap players
    (player1_proc, player2_proc) = (player2_proc, player1_proc)

# Stream polling objects
polling = [ poll(), poll()]
polling[0].register(player[0].stdout.fileno(), POLLIN)
polling[1].register(player[1].stdout.fileno(), POLLIN)

def handler(signum, frame):
    """Signal handler callback function. Called when registered signal is fired

    The handler is provided the signal number and the interrupted stack frame"""
    raise IOError("Unable to open device")

# Henceforth, handler will be called when SIGALRM is received
signal(SIGALRM, handler)

def end_code(exit_code):
    """Cleanup and exit BM. Kill spawned processes"""
    if player[0].poll() is None:
        player[0].kill()
    if player[1].poll() is None:
        player[1].kill()
    if popen_val_obj.poll() is None:
        popen_val_obj.kill()
    exit(exit_code)


# Output and corresp intermediate_string
player_output = ["", ""]
try:
    for i in range(51):
        if not player[i%2].poll():
            if i == 0:
                player[0].stdin.write("1\n")
                player[1].stdin.write("0\n")
            event_list = polling[i%2].poll(time_limit[i%2])
            if event_list and event_list[0][1] is POLLIN:
                try:
                    alarm(1)
                    player_output[0] = player[i%2].stdout.readline()
                    alarm(0)
                    player_output[1] = parser_func(player_output[0], popen_val_obj)
                    logfile.write('v,' + str((i+1)%2) + ',' + player_output[i%2])
                    player[(i+1)%2].stdin.write(player_output[2])
                except EndGameError as end_ev:
                    log_file.write(str(end_ev))
                    end_code(end_ev.winner)
                except ValueError as v:
                    log_file.write('l,' + str((i+1)%2) + ',' + player_output[i%2].rstrip('\n') + ',' + str(v))
                    end_code(102-(i%2))
                except IOError as e:
                    log_file.write('i,' + str((i+1)%2) + ',' + str(e))
                    end_code(102-(i%2))
            else:
                log_file.write('i,1,No I/O detected')
                end_code(102-(i%2))
        else:
            log_file.write('i,1,Premature termination')
            end_code(102-(i%2))
    else:
        log_file.write('i,0,Match did not terminate')
        end_code(100)
except Exception as e:
    print e
    end_code(255)
