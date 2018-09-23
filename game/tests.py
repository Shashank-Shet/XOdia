from django.test import TestCase
from py_compile import compile
from subprocess import check_output, CalledProcessError
from .__init__ import path
from shutil import copyfile
# Create your tests here.

bot_path = path + "files/bot"
stdbot_path = path + "sandbox/volume/BM/stdbot"
exec_path = path + "sandbox/volume/bots/"

def compileTest1(id1, ext1):
    bot1_path = bot_path + str(id1) + '.' + ext1
    list1 = []
    if ext1=="cpp":
        list1 = ["g++", "-o", str(id1), bot1_path]
    elif ext1=="c":
        list1 = ["gcc", "-o", str(id1), bot1_path]
    try:
        if not ext1=="py":
            check_output(list1, cwd=exec_path)
        else:
            compile(bot1_path, doraise=True, cfile=exec_path + str(id1))
    except:
        return 1

def compileTest2(id2, ext2):
    bot2_path = bot_path + str(id2) + '.' + ext2
    list2 = []
    if ext2=="cpp":
        list2 = ["g++", "-o", str(id2), bot2_path]
    elif ext2=="c":
        list2 = ["gcc", "-o", str(id2), bot2_path]
    try:
        if not ext2=="py":
            check_output(list2, cwd=exec_path)
        else:
            compile(bot2_path, doraise=True, cfile=exec_path + str(id2))
    except:
        return 2


def parseCompileTest(id1, ext1, id2, ext2):
    result = compileTest1(id1, ext1)
    if result==1:
        return "Syntactical errors are present in your bot."
    if id2=="s":
        # copyfile(stdbot_path, exec_path + "player2")
        return None

    result = compileTest2(id2, ext2)
    if result==2:
        return "Syntactical errors are present in your opponent's bot."
    return None
