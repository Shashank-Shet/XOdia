from .__init__ import path, django_log_file
from subprocess import call
import subprocess
from .models import Profile as MyUser
from shutil import move, copyfile
from .outSB import SandboxInit
from django.contrib.auth.models import User
bot_path = path + "files/"
match_path = path + "matches/"
executables_path = path + "sandbox/volume/bots/"
logfile_src_path = path + "sandbox/volume/matches/log"
errfile_src_path = path + "sandbox/volume/matches/error"


class SandboxRequest:
    def __init__(self, **kwargs):
        # bot1_path = kwargs["bot1_path"]
        # bot2_path = kwargs["bot2_path"]
        self.user1_id = kwargs["user1_id"]
        self.user2_id = kwargs["user2_id"]
        self.bot1_ext = kwargs["bot1_ext"]
        self.bot2_ext = kwargs["bot2_ext"]
        self.identifier_string = str(self.user1_id) + 'v' + str(self.user2_id)
        self.reverse_identifier_string = str(self.user2_id) + 'v' + str(self.user1_id)

    def runSandbox(self, marking_scheme):
        # call(["python", "BM.py", self.bot1_ext, self.bot2_ext], cwd=sandbox_path)
        # print "Reached here"
        id1 = self.user1_id
        id2 = self.user2_id
        # django_log_file.write("Request:"+self.identifier_string+'\n')
        copyfile(executables_path + str(id1), executables_path + "player1")
        copyfile(executables_path + str(id2), executables_path + "player2")

        subprocess.Popen(['chmod','u+x',executables_path + "player1"], stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        subprocess.Popen(['chmod', 'u+x', executables_path + "player2"], stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE, stderr=subprocess.PIPE)


        f = open("check_file", 'a')
        f.write("Request:"+self.identifier_string+'\n')
        f.close()
        winner_of_match_1 = SandboxInit(self.bot1_ext, self.bot2_ext, self.identifier_string, "False")
        if (self.identifier_string == self.reverse_identifier_string) or (winner_of_match_1==255):
            # f.write("Here\n")
            print("Temp" , logfile_src_path + self.identifier_string)

            move(logfile_src_path + self.identifier_string, match_path + "log" + self.identifier_string)
            move(errfile_src_path + self.identifier_string, match_path + "error" + self.identifier_string)
            return
        winner_of_match_2 = SandboxInit(self.bot1_ext, self.bot2_ext, self.reverse_identifier_string, "True")
        if winner_of_match_2 == 102:
            winner_of_match_2 = 101
        elif winner_of_match_2 == 101:
            winner_of_match_2 = 102
        # django_log_file.write(str(winner_of_match_1)+'\n')
        # django_log_file.write(str(winner_of_match_2)+'\n')
        f = open("check_file", 'a')
        f.write(str(winner_of_match_1) + '\n')
        f.write(str(winner_of_match_2) + '\n')
        if not 's' in self.identifier_string:
            marking_scheme(winner_of_match_1)
            marking_scheme(winner_of_match_2)
        self.relocate_log_files()

    def relocate_log_files(self):
        move(logfile_src_path + self.identifier_string, match_path + "log" + self.identifier_string)
        move(logfile_src_path + self.reverse_identifier_string, match_path + "log" + self.reverse_identifier_string)
        move(errfile_src_path + self.identifier_string, match_path + "error" + self.identifier_string)
        move(errfile_src_path + self.reverse_identifier_string, match_path + "error" + self.reverse_identifier_string)

    def stage2_marking(self, winner_of_match):
        my_myuser_obj = User.objects.get(pk=self.user1_id)
        opponent_myuser_obj = User.objects.get(pk=self.user2_id)
        if winner_of_match == 100:  # If draw occurs
            my_myuser_obj.userprofile.gdrawn += 1
            opponent_myuser_obj.userprofile.gdrawn += 1
            my_myuser_obj.userprofile.points +=1
            opponent_myuser_obj.userprofile.points += 1
        # if requester has won
        elif winner_of_match == 101:
            my_myuser_obj.userprofile.points += 3
            my_myuser_obj.userprofile.gwon += 1
            opponent_myuser_obj.userprofile.glost += 1
        # If requester has lost
        elif winner_of_match == 102:
            opponent_myuser_obj.userprofile.points += 3
            my_myuser_obj.userprofile.glost += 1
            opponent_myuser_obj.userprofile.gwon += 1
        my_myuser_obj.save()
        opponent_myuser_obj.save()
        my_myuser_obj.userprofile.save()
        opponent_myuser_obj.userprofile.save()

    def stage3_marking(self, winner_of_match):
        my_myuser_obj = User.objects.get(pk=self.user1_id)
        opponent_myuser_obj = User.objects.get(pk=self.user2_id)

        if winner_of_match == 100:
            my_myuser_obj.userprofile.points += 1
            opponent_myuser_obj.userprofile.points += 1
            my_myuser_obj.userprofile.gdrawn += 1
            opponent_myuser_obj.userprofile.gdrawn += 1
        elif winner_of_match == 101:
            my_myuser_obj.userprofile.points += 2
            my_myuser_obj.userprofile.gwon += 1
            opponent_myuser_obj.userprofile.glost += 1
        elif winner_of_match == 102:
            opponent_myuser_obj.userprofile.points += 2
            my_myuser_obj.userprofile.glost += 1
            opponent_myuser_obj.userprofile.gwon += 1
        my_myuser_obj.update()
        opponent_myuser_obj.update()
        my_myuser_obj.userprofile.update()
        opponent_myuser_obj.userprofile.update()

    def __str__(self):
        return self.identifier_string
