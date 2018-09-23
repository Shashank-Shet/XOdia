
#	-------------------------------------------  Overview of Control Flow  -------------------------------------------------
#
#	Xodia control flow(Stage 2) -
#	1) User submits a bot through the front-end, it is accecpted by django & stored in folders accordingly...
#	2) User requests a match through the front-end, django receives the request and in turn calls sandbox (outSB.py)
#	3) outSB.py creates the container & invokes the inner sandbox code (inSB.py)
#	4) inSB.py then calls Bot Management
#	5) Bot Management then runs bot1, bot2(the 2 bots in the match) & Validation and connects their inputs and outputs
#	6) If the match executes without errors, the output is stored in a log file which is rendered by the front-end and shown to the user


#	-------------------------------------------  Overview of outSB.py  -------------------------------------------------
#
#	This is a MODULE(a library) that we create for django, that's why we've written our code completely in functions, more on that later...
#	Control flow -
#	1) The Django code calls SandboxFunc() with the foll. args:-
#		arg1 = bot1.cpp, arg2 = bot2.cpp, id1 = userid of user1, id2 = userid of user2, player_string = unique string for each user
#		(arg1 and arg2 can have any name set by the user, and any extention - .c .cpp .py .py3)
#		(we name all our log files based on arg3, arg4 & arg5)
#	2) Our main objective is to spawn a container with the desired limits and pass the arguments, inside the container
#	3) Secondary objective is to limit the overall match time, if it exceeds the time, we kill the container - refer wait_timeout()
#	( BM will take care of the time limits of individual moves & also the amount of moves, but as a secondary protection - we limit the match time)
#

#	At a first glance, ignore anything with "sb_match_log" - they're log files created for debugging purposes
#	And ignore the paths, just remeber that we're using absolute paths not relative (creates less of a headache during deployment)
#	*** Since we're dealing with a lot of process, some of which are isolated inside the container, our main communication media are LOG FILES ***

import subprocess
import sys
import time
import SButils
from SBglobals import current_path, volume_path, sandbox_log_path, sandbox_log_name
from .__init__ import django_log_file
timer_flag = 0

#time limit for the whole match - Wait for a process to finish, or raise exception after timeout to kill the container
#only use this function for Popen() as it uses poll() to check the status of process(container)
def wait_timeout(proc, seconds, logfile_name, timer_flag):
    cidfile_name = sandbox_log_path + '/cont'+logfile_name

    #proc = Popen() object, seconds = max. match time, other args = for file naming conventions
    sb_match_log = open(sandbox_log_name,'a')

    start = time.time()
    end = start + seconds
    interval = 0.5		#0.25

    while True:
        try:
            result = proc.poll()					#only for subprocess commands
            if result is not None:
                sb_match_log.close()
                return result
            if time.time() >= end:
                raise RuntimeError("Match timed out")
                sb_match_log.write("timer running, time remaining = "+str(end-time.time())+"secs\n")
            time.sleep(interval)


        except RuntimeError as e:
            timer_flag = 1
            sb_match_log.write(e+'\n')

            file1 = open(cidfile_name, 'r')
            id = file1.readline()
            file1.close()

            #proc.kill() won't work here, we'll use docker's own mechanism to stop the container
            b = subprocess.Popen(['docker', 'stop', id], stdout = subprocess.PIPE, stderr = subprocess.PIPE)			#soft kill - max time for kill = 10 secs
            #b = subprocess.Popen(['docker', 'kill', id], stdout = subprocess.PIPE, stderr = subprocess.PIPE)		#for immediate kill
            [out, err] = b.communicate()

            sb_match_log.write('container stopped\n')
            sb_match_log.write('Timeout Out: ' + out+'\n')
            sb_match_log.write('Timeout Err: ' + err+'\n')
            #sb_match_log.write('\n"The match has timed out!" has beenwritten to the "error" log file')

            #This file is read by django for it to know that the match has timed out
            file2 = open(volume_path+'/matches/error'+logfile_name, 'w')		#***will overrite previous error file***
            file2.write("The match has timed out!\n")
            file2.close()
            sb_match_log.close()
            return



def SandboxFunc(ext1,ext2,logfile_name,flip):

    cidfile_name = sandbox_log_path + '/cont'+logfile_name

    print "TempTempTemp"
    print ext1,ext2,logfile_name,flip
    print "HAHAHAHAHA",cidfile_name
    #flip = "False"
    # ------------ Main command to spawn the container -------------
    # Notice that we're not using "sudo docker run", since we don't want to give root priviledges to the bots as processes spawned by root, have root priviledges
    # Here we're mounting 3 volumes -
    # 	1) The first one contains our modules - inSB.py, BM and validation
    #	2) The second one contains the bots submitted by user
    #	3) The third one contains the match log files generated inside the container
    # --cidfile creates a file with the container-id of the newly creted container - we'll need this to delete the container after the match and also for debugging
    #a = subprocess.Popen(['docker', 'run', '-m',  '70M', '--memory-swappiness', '0', '-v', volume_path + ':/volume/', '-v', volume_path + 'bots:/volume/bots/', '-v', volume_path + 'matches/:/volume/matches/', '--cidfile', cidfile_name, '--pids-limit', '15', '--ulimit',  'nofile=100:100', '--ulimit', 'nproc=800:1000', '-w', '/volume/BM/', 'xodiaimg', 'python', 'inSB.py',ext1,ext2,logfile_name,flip], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Volume : ",volume_path)
    a = subprocess.Popen(['docker', 'run', '-m',  '120M', '--memory-swappiness', '0', '-v', volume_path + ':/volume', '--cidfile', cidfile_name, '--pids-limit', '15', '--ulimit',  'nofile=100:100', '--ulimit', 'nproc=800:1000', '-w', '/volume/BM/', 'xodiaimg', 'python2', 'inSB.py',ext1,ext2,logfile_name,flip], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    print("HHHH" , a)
    #Alternatives -
     # a = subprocess.Popen(['sudo docker run -m 100M --memory-swappiness 0 -v ~/Sandbox/volume:/volume --ulimit nofile=100:100 --ulimit nproc=1000:1000 -w /volume/BM3/ xodiatestfinal3 python inSB4.py' +' ' + arg1 + ' ' + arg2], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #I removed the -itd since we don't want to run bash after this python code, so the -i keeps the input open and the sys.stdin.read() probably expects an input from the terminal, ignoring the ones sent from its parent process, thats why we need the -d to isolate the stdin from the terminal so that it only has one input to take - the input from its parent. removing -itd solves the whole problem and also as a bonus it prints everything on the main terminal not on its pseudo tty, so we  can actually see the output and error messages of the container using print out and print err unlike last time


#	sb_match_log.write('container started\n')
#	sb_match_log.close()

    wait_timeout(a, 60, logfile_name, timer_flag)	# match time limit = 300sec

    [out, err] = a.communicate()
    """sb_match_log = open(sandbox_log_name,'a')

    sb_match_log.write('outSB Out: ' + out+'\n')
    sb_match_log.write('outSB Err: ' + err+'\n')
    sb_match_log.write("Outsb end\n")

    sb_match_log.close()"""
    #f = open("/home/neeraj/Neeraj/Xodia_New/xodia2_phase2/check_file", 'a')
    #f.write("BM ret_code:" + str(a.returncode) + '\n')
    #f.close()
    return a.returncode




def SandboxInit(ext1, ext2, logfile_name, flip):
    cidfile_name = sandbox_log_path + '/cont'+logfile_name
    print(sandbox_log_path)
    print(cidfile_name)


    """sb_match_log = open(sandbox_log_name,'a')
    sb_match_log.write("*Match: "+logfile_name+"*\n")
    sb_match_log.close()"""

    SButils.DeleteFileIfExists(cidfile_name)

    match_outcome = SandboxFunc(ext1, ext2, logfile_name, flip)

    SButils.DeleteCont(cidfile_name, logfile_name, match_outcome, timer_flag)

    """sb_match_log = open(sandbox_log_name,'a')
    sb_match_log.write("match_outcome = " + str(match_outcome)+'\n')
    sb_match_log.write("\n\n\n\n\n")
    sb_match_log.close()"""

    return match_outcome

#if __name__ == "__main__":
#	SandboxInit(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    # an example command - python outSB.py cpp cpp 1_2 0



#future_addition1 - depending on extension of arg1 and arg2(.c .java or .py), change the ulimits of container - assign a base value and a value based on the type of file to be added, limit = base value + value_arg1 + value_arg2
