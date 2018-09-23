import subprocess, os
#from outSB import sandbox_log_path, current_path, sandbox_log_name		#***creates a circular import
from SBglobals import sandbox_log_path, current_path, sandbox_log_name

def DeleteFileIfExists(filename):
#	stuff = open(sandbox_log_name,'a')

	if(os.path.exists(filename)):
		a = open(filename,"r")
		b = a.readline()
#		stuff.write(filename + " exists, contents are: " + b+'\n')
		os.remove(filename)
#		stuff.write('***'+filename + " deleted\n")
	else:						#If the file does not exist, do nothing
		pass
#		stuff.write(filename + " could not be deleted(it may not exist)\n")
#	stuff.close()

def DeleteCont(cidfile_name, logfile_name, match_outcome, timer_flag):
	#a = subprocess.Popen(['docker', 'ps', '-lq'], stdout=subprocess.PIPE)
	#cont = a.stdout.read()
	#cont = cont.rstrip()				#removing newline

#	stuff = open(sandbox_log_name,'a')
	if(not os.path.exists(cidfile_name)):				#ch if cont file exists, else opening it gives an error
#		stuff.write('\nNot deleting container or cidfile -'+cidfile_name+' does not exist\n')
#		stuff.close()
		return
	#if match does not terminate successfully, don't delete the container or the cidfile - usefull for finding the error in the match
	if(os.stat(current_path + "/../sandbox/volume/matches/error" + logfile_name).st_size!=0):
#		stuff.write("Not deleting container or cidfile - Error file is not empty - Match terminated with an error\n")
#		stuff.close()
		return
	if(match_outcome == 255):
#		stuff.write("Not deleting container or cidfile - BM returned the error code: "+match_outcome+"\n")
#		stuff.close()
		return
	if(timer_flag == 1):
#		stuff.write("Not deleting container or cidfile - Match timed out\n")
#		stuff.close()
		return



	file1 = open(cidfile_name, 'r')			#contains the container id
	cont_id = file1.readline().rstrip()
	file1.close()

	b = subprocess.Popen(['docker', 'rm', cont_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#	stuff.write("Container deleted - cid: "+cont_id+'\n')
	[out, err] = b.communicate()
	b.wait()

#	stuff.write('DeleteCont Out: ' + out+'\n')
#	stuff.write('DeleteCont Err: ' + err+'\n')

	DeleteFileIfExists(cidfile_name)
#	stuff.close()
