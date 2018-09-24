# run this code with follwing command line args
# argv[1] -> bot1 path (absolute)
# argv[2] -> bot2 path (absolute)
# argv[3] -> log file path (absolute)

from subprocess import call, Popen, PIPE
from select import poll, POLLIN
from signal import signal, alarm, SIGALRM
from sys import exit, argv
from val_parser import parser_func, EndGameError

time_limits = {
	"cpp": 2000,
	"c": 2000,
	"py": 6000,
}


ext1 = argv[1]
ext2 = argv[2]

# print argv[3]

plist1 = ["prlimit", "-p", ""]
plist2 = ["prlimit", "-p", ""]

log_file = open( '../matches/log' + argv[3] , 'w')

#NOTE: Compiling will not be done in the BM code in the final project. This is only here for convenience
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

# Run bots
call(plist1)
call(plist2)

if argv[4] == "True":               # Swap players
	(player1_proc, player2_proc) = (player2_proc, player1_proc)

# Stream polling objects
poll_obj1 = poll()
poll_obj2 = poll()

poll_obj1.register(player1_proc.stdout.fileno(), POLLIN)
poll_obj2.register(player2_proc.stdout.fileno(), POLLIN)

time_limit1 = time_limits[ext1]
time_limit2 = time_limits[ext2]

def handler(signum, frame):
	"""Signal handler callback function. Called when registered signal is fired

	The handler is provided the signal number and the interrupted stack frame"""
	raise IOError("Unable to open device")

# Henceforth, handler will be called when SIGALRM is received
signal(SIGALRM, handler)

def end_code(exit_code):
	"""Cleanup and exit BM. Kill spawned processes"""
	if player1_proc.poll() is None:
		player1_proc.kill()
	if player2_proc.poll() is None:
		player2_proc.kill()
	if popen_val_obj.poll() is None:
		popen_val_obj.kill()
	exit(exit_code)


try:
	if not player1_proc.poll() and not player2_proc.poll():
		player1_proc.stdin.write("1\n")
		player2_proc.stdin.write("0\n")#was 2
		#This poll method is again different. It belongs to the poll object
		#It represents the time which the poll object will wait to receive an input
		temp = poll_obj1.poll(time_limit1)
		if temp and temp[0][1] is POLLIN:       #If the occurred event was a POLLIN. Ideally, no other event should occur
			try:
				alarm(1)
				p = player1_proc.stdout.readline()
				alarm(0)
				intermediate_string = parser_func(p, popen_val_obj)
				log_file.write('v,1,' + p)
				player2_proc.stdin.write(intermediate_string)
			except EndGameError as end_ev:
				log_file.write(str(end_ev))
				end_code(end_ev.winner)
			except ValueError as v:
				log_file.write('l,1,' + p.rstrip('\n') + ',' + str(v))
				end_code(102)
			except IOError as e:
				log_file.write('i,1,' + str(e))
				end_code(102)
		else:
			log_file.write('i,1,No I/O detected')
			end_code(102)
	else:
		log_file.write('i,1,Premature termination')
		end_code(102)

	if not player1_proc.poll() and not player2_proc.poll():
		temp = poll_obj2.poll(time_limit2)
		if temp and temp[0][1] is POLLIN:
			try:
				alarm(1)
				p = player2_proc.stdout.readline()
				alarm(0)
				intermediate_string = parser_func(p, popen_val_obj)
				log_file.write('v,0,' + intermediate_string)
				player1_proc.stdin.write(intermediate_string)
			except EndGameError as end_ev:
				log_file.write(str(end_ev))
				end_code(end_ev.winner)
			except ValueError as v:
				log_file.write('l,0,' + intermediate_string.rstrip('\n') + ',' + str(v))#was 2
				end_code(101)
			except IOError as e:
				log_file.write('i,0,' + str(e))
				end_code(101)
		else:
			log_file.write('i,0,No I/O detected')
			end_code(101)
	else:
		log_file.write('i,0,Premature termination')
		end_code(101)

	#The below code is for the while(1) implementation. Used a for loop to run a max of 50 iterations
	for i in range(50):
		if not player1_proc.poll() and not player2_proc.poll():
			temp = poll_obj1.poll(time_limit1)
			if temp and temp[0][1] is POLLIN:
				try:
					alarm(1)
					p = player1_proc.stdout.readline()
					alarm(0)
					intermediate_string = parser_func(p, popen_val_obj)
					log_file.write('v,1,' + p)
					player2_proc.stdin.write(intermediate_string)
				except EndGameError as end_ev:
					log_file.write(str(end_ev))
					end_code(end_ev.winner)
				except ValueError as v:
					log_file.write('l,1,' + p.rstrip('\n') + ',' + str(v))
					end_code(102)#was 102
				except IOError as e:
					log_file.write('i,1,' + str(e))
					end_code(102)
			else:
				log_file.write('i,1,No I/O detected')
				end_code(102)
		else:
			log_file.write('i,1,Premature termination')
			end_code(102)

		if not player1_proc.poll() and not player2_proc.poll():
			temp = poll_obj2.poll(time_limit2)
			if temp and temp[0][1] is POLLIN:
				try:
					alarm(1)
					p = player2_proc.stdout.readline()
					alarm(0)
					intermediate_string = parser_func(p, popen_val_obj)
					log_file.write('v,0,' + intermediate_string)#was 2
					player1_proc.stdin.write(intermediate_string)
				except EndGameError as end_ev:
					log_file.write(str(end_ev))
					end_code(end_ev.winner)
				except ValueError as v:
					log_file.write('l,0,' + intermediate_string.rstrip('\n') + ',' + str(v))
					end_code(101)
				except IOError as e:
					log_file.write('i,0,' + str(e))
					end_code(101)
			else:
				log_file.write('i,0,No I/O detected')
				end_code(101)
		else:
			log_file.write('i,0,Premature termination')
			end_code(101)
	else:
		log_file.write('i,0,Match did not terminate')
		end_code(100)#was 100
except Exception as e:
	print e
	end_code(255)
end_code()
