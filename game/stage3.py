from .__init__ import path
from models import MyUser
from RequestQueue import request_queue
from django.contrib.auth.models import User
from .tests import compileTest1, compileTest2
from .Sandbox import SandboxRequest


def resetScores():
    query_set = MyUser.objects.all()
    for myuser_obj in query_set:
        myuser_obj.score = 0
        myuser_obj.wins = 0
        myuser_obj.losses = 0
        myuser_obj.draws = 0
        myuser_obj.update()



def startLeague():
    request_queue.clear()
    query_set_list = list(MyUser.objects.all())
    iterator1 = 0
    while iterator1 < len(query_set_list) - 1:
        qs_obj1 = query_set_list[iterator1]
        res = compileTest1(qs_obj1.user_object.pk, qs_obj1.bot_ext)
        if not res is None:
            print str(query_set_list[iterator1].user_object.pk) + " Eliminated"
            query_set_list.pop(iterator1)
            continue
        iterator2 = iterator1 +1
        while iterator2 < len(query_set_list):
            qs_obj2 = query_set_list[iterator2]
            res = compileTest2(qs_obj2.user_object.pk, qs_obj2.bot_ext)
            if not res is None:
                print str(query_set_list[iterator2].user_object.pk) + " Eliminated"
                query_set_list.pop(iterator2)
                continue
            print qs_obj1.pk, qs_obj2.pk
            req_obj = SandboxRequest(
            user1_id=qs_obj1.user_object.pk,
            user2_id=qs_obj2.user_object.pk,
            bot1_ext=qs_obj1.bot_ext,
            bot2_ext=qs_obj2.bot_ext,
            )
            req_obj.runSandbox(req_obj.stage3_marking)
            iterator2 += 1

        iterator1 += 1
