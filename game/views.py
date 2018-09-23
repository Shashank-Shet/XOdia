from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Profile
from django.db import IntegrityError
import urllib
import urllib2
import json
from django.conf import settings
from django.core.files import File
import os
from .file_handle import file_storage_handle
from .__init__ import path
import requests
from os.path import isfile
from .Sandbox import SandboxRequest
from .tests import parseCompileTest
from .RequestQueue import RequestQueue, request_queue
from django.http import JsonResponse
from sys import argv




match_path = path + "matches/"
match_runner = RequestQueue()      # parallel thread which executes match requests one at a time
if "runserver" not in argv:
	match_runner.daemon = True         # enable Ctrl-C to terminate the whole program + thread
match_runner.start() 

# Create your views here.
class SignupView(View):
    template_name = 'game/signUp.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        data_set = request.POST
        username = data_set["username"]
        email = data_set["email"]
        first_name = data_set["name"]
        phone = data_set["phone"]
        password = data_set["password"]
        college = data_set["college"]
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = json.load(response)
        if result['success']:
            myuse_obj = Profile()

            try:
                myuse_obj.create(username=username, email=email, password=password, first_name=first_name, phone=phone,
                                 college=college)
                myuse_obj.create_myuser()
                myuse_obj.save()
            except IntegrityError:
                return render(request, self.template_name,
                              {'err_msg': "Username is already taken!", 'first_name': first_name, 'email': email,
                               'phone': phone, 'college': college})
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('game:postlogin')
            return redirect('game:signup')
        else:
            return render(request, self.template_name,
                          {'err_msg2': 'Invalid Captcha', 'first_name': first_name,
                           'email': email, 'username': username, 'phone': phone, 'college': college})


class GridView(View):
    template_name = "game/submit_ui.html"

    def get(self, request):
        au = request.user.is_authenticated
        pro = User.objects.all()
        return render(request, self.template_name, {'au': au, 'username': request.user.username, 'pro': pro})

    def post(self, request):
        pro = User.objects.all()
        au = request.user.is_authenticated
        if not request.user.is_authenticated:
            return render(request, self.template_name, {'suc': 'You must log in to upload a file', 'au': au, 'pro':pro, 'username': request.user.username})
        elif 'upload' in request.POST:
            return self.bot_upload(request)
        elif 'matchreq' in request.POST:
            print("done")
            return self.match_request(request)
        elif 'viewlog' in request.POST:
            return self.view_request(request)
        else:
            return redirect('game:ui')
            
    def bot_upload(self, request):
        pro = User.objects.all()
        au = request.user.is_authenticated
        if request.FILES:
            file = request.FILES['botup']

            result = file_storage_handle(file)



            if result == 0:
                curr_obj = request.user
                filename = file.name
                ext = filename.split('.')[-1]
                f = open(curr_obj.userprofile.bot_path + '.' + curr_obj.userprofile.bot_ext, 'w')
                os.rename(curr_obj.userprofile.bot_path + '.' + curr_obj.userprofile.bot_ext,
                          curr_obj.userprofile.bot_path + '.' + ext)

                curr_obj.userprofile.bot_ext = ext
                # print(f)
                # print(file)
                # curr_obj.save()
                # print(curr_obj.pk)
                # print(curr_obj.userprofile.bot_ext)
                # print(curr_obj.userprofile.bot_path)
                for line in file.chunks():
                    f.write(line)
                    #print(line)
                f.close()
            else:
                return render(request, self.template_name, {'suc': 'File should be a C, CPP or Python file', 'pro':pro, 'au':au, 'username': request.user.username})
            try:
                curr_obj.userprofile.save()
            except:
                return render(request, self.template_name, {'suc': 'Upload Unsuccessful! Please Try Again', 'au': au, 'pro': pro, 'username': request.user.username})
            return render(request, self.template_name, {'suc': 'Upload Successful!', 'au': au, 'pro': pro, 'username': request.user.username})
        else:
            return render(request, self.template_name, {'au': au, 'suc': 'Please upload a file','pro':pro, 'username': request.user.username})


    def match_request(self,request):
        pro = User.objects.all()
        au = request.user.is_authenticated
        curr_obj = request.user
        opp_id = request.POST['oppid']
        #p2flag = request.POST.get('p2flag')

        if not opp_id:
            return render(request, self.template_name, {'suc':'Please Select an opponent', 'au':au,'pro':pro, 'username': request.user.username})
        my_id = curr_obj.pk
        #if not p2flag:
        match = str(my_id) + 'v' + opp_id
        reverse_match = opp_id + 'v' + str(my_id)
        #else:
           # match = opp_id + 'v' + str(my_id)
            #reverse_match = str(my_id) + 'v' + opp_id
            
        for match_temp in request_queue:
            if match_temp.identifier_string == match:
                return render(request,self.template_name, {'suc': 'Match is already in queue', 'au': au,'pro':pro, 'username': request.user.username})
        
        ext1 = curr_obj.userprofile.bot_ext
        opp_user = User.objects.get(pk=int(opp_id))
        ext2 = opp_user.userprofile.bot_ext


        #if not p2flag:
        result = parseCompileTest(my_id, ext1, opp_id, ext2)
        #else:
            #result = parseCompileTest(opp_id, ext2, my_id, ext1)
        if result is not None:
            print(result)
            return render(request, self.template_name, {'suc': result, 'au': au,'pro':pro, 'username': request.user.username})
        if os.path.exists(match_path + 'log' + match):
            os.remove(match_path + 'log' + match)
            os.remove(match_path + 'error' + match)
        if os.path.exists(match_path+ 'log' + reverse_match):
            os.remove(match_path+ 'log' + reverse_match)
            os.remove(match_path+ 'error' + reverse_match)
        match_obj = SandboxRequest(user1_id=my_id, user2_id=opp_id, bot1_ext=ext1, bot2_ext=ext2)
        print("Temp",match_obj)

        request_queue.append(match_obj)

        match_runner.set_flag()
        
        return render(request, self.template_name, {'suc':'Match requested!', 'au':au, 'pro':pro, 'username': request.user.username})

    def view_request(self,request):
        pro = User.objects.all()
        au = request.user.is_authenticated
        my_id = request.user.pk
        opp_id = request.POST['oppid']
        if not opp_id:
            return render(request, self.template_name, {'suc':'Please select opponent', 'au':au,'pro':pro, 'username': request.user.username})
        p2flag = request.POST.get('p2flag')
        if not p2flag:
            match = str(my_id) + 'v' + opp_id
            reverse_match = opp_id + 'v' + str(my_id)
        else:
            match = opp_id + 'v' + str(my_id)
            reverse_match = str(my_id) +'v' + opp_id
        #print(match)
        #print(reverse_match)
        log_path = match_path + 'log' + match
        print 'yguhg'
        print 'log path'
        error_path = match_path + 'error' + match
        rev_error_path = match_path + 'error' + reverse_match
        log_pass =''
        error_pass = ''
        if not os.path.isfile(error_path):
            print 'here'
            if not os.path.isfile(rev_error_path):
                print('wrong')
                return render(request, self.template_name, {'suc':'Match not processed yet','au':au,'pro':pro, 'username': request.user.username})
        #else:
            #error_path = rev_error_path

            #print(log_pass)
        if os.path.isfile(error_path):
            errorfile = open(error_path,'r')
            error_pass = errorfile.read().split('\n')
            print(error_path)

        if os.path.isfile(log_path):
            logfile = open(log_path, 'r')
            log_pass = logfile.read().split('\n')
            print(log_path)
            #print(error_pass)

        print log_path
        print error_path
        return render(request, self.template_name, {'au':au, 'log': log_pass, 'error':error_pass,'pro':pro, 'username': request.user.username})


class LeaderBoard(View):
    template_name = 'game/leader.html'

    def get(self, request):
        au = request.user.is_authenticated
        pro = Profile.objects.all().order_by('-points')
        return render(request, self.template_name, {'pro': pro,'au':au,'username':request.user.username})


def logoff(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('game:login')


class LogIn(View):
    template_name = 'game/prelogin.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('game:postlogin')
        return render(request, self.template_name, {})

    def post(self, request):
        data_set = request.POST
        username = data_set["username"]
        password = data_set["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('game:postlogin')
        else:
            return render(request, self.template_name, {'err_ms': "Invalid Username or Password!"})


class PostLogin(View):
    template_name = 'game/postlogin.html'

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name,
                          {'username': request.user.username, 'name': request.user.first_name,
                           'email': request.user.email}, )
        else:
            return redirect('game:login')

class playableUI(View):
    template_name = 'game/playable_ui.html'

    def get(self, request):
        au = request.user.is_authenticated
        return render(request, self.template_name, {'au':au, 'username':request.user.username})
