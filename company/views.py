from django.shortcuts import render
import pyrebase
from django.http import HttpResponse
import csv
from . import scripts
from django.contrib import auth
# Create your views here.

config = {
    "apiKey": "AIzaSyBvh9iylzZWC98LdyfGkNVhpN7bSmPsMQo",
    "authDomain": "envision-c5ff8.firebaseapp.com",
    "databaseURL": "https://envision-c5ff8.firebaseio.com",
    "projectId": "envision-c5ff8",
    "storageBucket": "envision-c5ff8.appspot.com",
    "messagingSenderId": "499710815066"
  }

firebase = pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()





def login(request):
    return render(request,"company/login.html")

def admin(request):
    cust=request.POST.get('user')
    email=request.POST.get('email')
    password=request.POST.get('pass')

    if(cust=="employee"):
        try:
            user=authe.sign_in_with_email_and_password(email,password)
        except:
            message="Please enter valid credentials"
            return render(request,"company/landing.html",{'message':message})

        data={
            'email':email,
        }
        return render(request,"company/admin.html",data)
    elif(cust=="customer"):
        try:
            user = authe.sign_in_with_email_and_password(email, password)
        except:
            message = "Email or password not valid"
            return render(request, "company/login.html",{"msg":message})

        session_id = user['idToken']
        request.session['uid'] = str(session_id)

        #getting company's name
        email_dict = database.child("email").get().val()
        c_name = list(email_dict.keys())[list(email_dict.values()).index(email)]


        #number of calls made
        calls = database.child('companies').child(c_name).child('aftercall').get().val()

        total_num_calls = scripts.count_total_calls(calls)

        daily_num_calls = scripts.count_daily_calls(calls)

        total_pos, daily_pos_calls = scripts.pos_calls(calls)

        total_neg = total_num_calls - total_pos

        #------------------------------------------------------------#
        #key = date
        #value = [neg, pos]
        daily_neg_calls = scripts.neg_calls(daily_num_calls, daily_pos_calls)
        #------------------------------------------------------------#

        """print(total_num_calls)
        print(total_pos)
        print(total_neg)
        print(daily_num_calls)
        print(daily_pos_calls)
        print(daily_neg_calls)"""

        return render(request, "company/welcome.html",{"c":c_name,"calls":calls,"t_pos":total_pos,"t_neg":total_neg,"d_pos":daily_pos_calls,"d_neg":daily_neg_calls,"d_num":daily_num_calls})





def file_upload(request):
    files=request.FILES.get('files')
    Cname=request.POST.get('c_name')
    file=files.read().decode("utf-8")
    lines = file.split("\n")
    len_csv=len(lines)-1
    cg,imei_list=distribution_helper_function(database,len_csv,Cname)
    _counter=0
    item=0
    #print(cg)
    sub_array_name=[]
    sub_array_phone=[]
    for i,line in enumerate(lines):
        line=str(line)
        line=line.split(',')
        if(len(line)>1 and _counter<cg and item<len(imei_list)-1 ):
            _counter=_counter+1
            sub_array_name.append((imei_list[item][0],line[0].rstrip()))
            sub_array_phone.append((imei_list[item][0],line[1].rstrip()))
            #print((imei_list[item][0],line[0].rstrip()))
            #data={'name':line[0].rstrip(),'phone':line[1].rstrip(),}
            #print(imei_list[item][0])
            #database.child('callers1').child(imei_list[item][0]).child('customers').update(data)
        elif(len(line)>1 and item==len(imei_list)-1):
            sub_array_name.append((imei_list[item][0],line[0].rstrip()))
            sub_array_phone.append((imei_list[item][0],line[1].rstrip()))
            #print((imei_list[item][0],line[0].rstrip()))
            #data={line[1].rstrip():{'name':line[0].rstrip()}}
            #print(imei_list[item][0])
            #database.child('callers1').child(imei_list[item][0]).child('customers').update(data)
        else:
            _counter=0
            item=item+1
    item=0
    x=0
    name_temp=[]
    temp=sub_array_name[0][0]
    for name in sub_array_name:
        if(name[0]==temp):
            name_temp.append(name[1])
        else:
            data={'name':name_temp}
            database.child('callers1').child(temp).child('customers').update(data)
            temp=name[0]
            name_temp=[]
            name_temp.append(name[1])
    data={'name':name_temp}
    database.child('callers1').child(temp).child('customers').update(data)
    phone_temp=[]
    temp=sub_array_name[0][0]
    for phone in sub_array_phone:
        if(phone[0]==temp):
            phone_temp.append(phone[1])
        else:
            data={'phone':phone_temp}
            database.child('callers1').child(temp).child('customers').update(data)
            temp=phone[0]
            phone_temp=[]
            phone_temp.append(phone[1])
    data={'phone':phone_temp}
    database.child('callers1').child(temp).child('customers').update(data)
    #print(sub_array_name)
    #print(sub_array_phone)
    return HttpResponse('')


def distribution_helper_function(database,csv_len,cname):
    nos=database.child('IMEI').get()
    nos=nos.val()
    imei=list(nos.items())
    ret_imei=[]
    for i in imei:
        if i[1]==cname:
            ret_imei.append(i)
    total_imei=len(ret_imei)
    change=csv_len//total_imei
    if(csv_len>total_imei):
        return change,ret_imei
    else:
        return change+1,ret_imei




def index(request):

    return render(request,"company/index.html")


def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = authe.sign_in_with_email_and_password(email, password)
    except:
        message = "Email or password not valid"
        return render(request, "signIn.html",{"msg":message})
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    #getting company's name
    email_dict = database.child("email").get().val()
    c_name = list(email_dict.keys())[list(email_dict.values()).index(email)]
    print("Company = " + c_name)

    #number of calls made
    calls = database.child('companies').child(c_name).child('aftercall').get().val()

    total_num_calls = scripts.count_total_calls(calls)

    daily_num_calls = scripts.count_daily_calls(calls)

    total_pos, daily_pos_calls = scripts.pos_calls(calls)

    total_neg = total_num_calls - total_pos

    #------------------------------------------------------------#
    #key = date
    #value = [neg, pos]
    daily_neg_calls = scripts.neg_calls(daily_num_calls, daily_pos_calls)
    #------------------------------------------------------------#

    """print(total_num_calls)
    print(total_pos)
    print(total_neg)
    print(daily_num_calls)
    print(daily_pos_calls)
    print(daily_neg_calls)"""

    return render(request, "company/welcome.html",{"c":c_name,"t_pos":total_pos,"t_neg":total_neg,"d_pos":daily_pos_calls,"d_neg":daily_neg_calls,"d_num":daily_num_calls})

def logout(request):
    auth.logout(request)
    return render(request, "company/login.html")