from typing import Collection
from django.contrib.auth.models import UserManager
from django.shortcuts import render,redirect

# importing password encryptor
from django.contrib.auth.hashers import make_password, check_password

# importing all app models
from todoapp.models import *

# importing django login athentications
from django.contrib.auth import authenticate, login, logout

# it is for filter only logined user can access user dashboard page
from django.contrib.auth.decorators import login_required


# other code - otp senting to mail
# import random
# import http.client
# from django.conf import settings

# def send_otp(mobile,otp):
#     # conn = http.client.HTTPSConnection("api.msg91.com")
#     # authkey=settings.authkey
#     # headers = { 'content-type': "application/json" }
#     # url='http://control.msg91.com/api/sendotp.php?otp'+otp+'&sender=ABC&message='+'Your otp is '+otp+'&mobile='+mobile+'&authkey='+authkey+'&country=91',
#     print("FUNCTION CALLED")
#     conn = http.client.HTTPSConnection("api.msg91.com")
#     authkey = settings.authkey
#     headers = { 'content-type': "application/json" }
#     url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message="+"Your otp is "+otp +"&mobile="+mobile+"&authkey="+authkey+"&country=91"
#     conn.request("GET", url , headers=headers)
#     res = conn.getresponse()
#     data = res.read()
#     print(data)
#     return None

# Create your views here.

# home page (getstart page)
def index(request):
    if request.user.is_authenticated:
        print('User Already logined')
        return redirect(todolist)

    return render(request,'index.html',{})

# user signup 
def signup(request):
    if request.user.is_authenticated:
        print('User Already logined')
        return redirect(todolist)
    else:
        if request.method=='POST':
            email=request.POST.get('s_email')
            password=request.POST.get('s_psd')
            confirm_psd=request.POST.get('confirm_psd')
            print(email)
            print(password)
            print(confirm_psd)

            if(email== '' or password==''):
                print('No value')
                return render(request,'signup.html',{'checker':'Please enter valid info...!','static_mail':email})

            elif(not password==confirm_psd):
                print('Password Missmatch')
                return render(request,'signup.html',{'checker':'Password Missmatch...!','static_mail':email})
                
            elif(not email.endswith('@gmail.com')):
                print('Invalid Email...!')
                return render(request,'signup.html',{'checker':'Invalid Email...!','static_mail':email})
                
            elif User.objects.filter(username=email).exists():
                print('User already exist')
                return render(request,'signup.html',{'checker':'User already exist..!.','static_mail':email})
            else:
                #making password encryption for login purpose(becz django weak password is not allowed in authentication)
                passEncrypted = make_password(password)

                # creating User table object
                auth_user=User()
                auth_user.username=email.lower()# lower() is for converting email uppercase letter to lower case letter
                auth_user.password=passEncrypted
                auth_user.save()
                print("Signup successful")

                return render(request,'login.html',{'checker':'Account Created Successfully.. Please Login..!'})
        


    return render(request,'signup.html',{})

# user login
def loginpage(request):
    if request.user.is_authenticated:
        print('User Already logined')
        return redirect(todolist)
    else:
        if request.method=='POST':
            email=request.POST.get('email')
            password=request.POST.get('password')
            print(email)
            print(password)

            if(email== '' or password==''):
                print('No value')
                return render(request,'login.html',{'checker':'Please enter valid info...!','static_mail':email})

            elif(not email.endswith('@gmail.com')):
                print('Invalid Email...!')
                return render(request,'login.html',{'checker':'Invalid Email...!','static_mail':email})
            
            else:
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    print('user login success')

                    # Collecting user all todo value
                    # todovalue=todo_db.objects.filter(email__contains=request.user) # this data is for showing todolist data in pages
                    # return render(request,'todolistpage.html',{'todovalue':todovalue})
                    return redirect(todolist) 

                else:
                    return render(request,'login.html',{'checker':'Invalid Username or Password','static_mail':email})

    return render(request,'login.html',{})

# user todo's adding area
@login_required(login_url="/login")
def add(request):
    if request.method=='POST':
        taskdata=request.POST.get('taskdata')
        datetime=request.POST.get('datetime')
        priority=request.POST.get('priority')
        print(taskdata)
        print(datetime)
        print(priority)

        if (taskdata == '' or datetime == '' or priority == ''):
            print('No value')
            return render(request,'addpage.html',{'checker':'Please enter valid data...!'})

        elif ( len(taskdata)>100 ):
            print('Limit 100 Crossed')
            return render(request,'addpage.html',{'checker':'You cross the limit of data (100 above characters reached)...!'})
        
        elif todo_db.objects.filter(email=request.user,tasktimedate=datetime).exists(): #task=taskdata priority=priority
            print('same data found')

            # Filtering values from todo_db
            # todo_high=todo_db.objects.filter(email__contains=request.user,priority='High') # Fetching high priority from todo db
            # todo_medium=todo_db.objects.filter(email__contains=request.user,priority='Medium') # Fetching medium priority from todo db
            # todo_normal=todo_db.objects.filter(email__contains=request.user,priority='Normal') # Fetching normal priority from todo db

            # context={'todo_high':todo_high,'todo_medium':todo_medium,'todo_normal':todo_normal,
            # 'checker':'Same data found in your Todo List...! Please Edit or Delete Your Todo List'}

            context={'checker':'Same date and time is found in your Todo List...! Please go to todo List',
            'taskdata':taskdata,'datetime':datetime,'priority':priority}

            return render(request,'addpage.html',context)# only pass context value, because render only support one dictionary value

        else: # Todo's saving area //////////////////////
            user_db=User.objects.filter(username__contains=request.user)
            for userid in user_db:
                print(userid.id,'Userid')
            
            todo_obj=todo_db()
            todo_obj.login_id=userid #saving User id to todo_db
            todo_obj.task=taskdata.capitalize()
            todo_obj.tasktimedate=datetime
            todo_obj.status='pending'
            todo_obj.priority=priority
            todo_obj.email=request.user
            todo_obj.save()
            print('todo save successfully')

            todo_delete_id=User.objects.get(username__contains=request.user)# passing user id from auth user table for delete all usertodo values
            print(todo_delete_id.id,'my id')

            # Filtering values from todo_db
            todo_high=todo_db.objects.filter(email__contains=request.user,priority='High') # Fetching high priority from todo db
            todo_medium=todo_db.objects.filter(email__contains=request.user,priority='Medium') # Fetching medium priority from todo db
            todo_normal=todo_db.objects.filter(email__contains=request.user,priority='Normal') # Fetching normal priority from todo db
            todo_completed=todo_db.objects.filter(email__contains=request.user,priority='Completed') # Fetching completed priority from todo db

            context={'todo_delete_id':todo_delete_id,'todo_high':todo_high,'todo_medium':todo_medium,'todo_normal':todo_normal,
            'todo_completed':todo_completed,'checker':'Todo saved succesfully..'}

            return render(request,'todolistpage.html',context) # only pass context value, because render only support one dictionary value
             # Todo's saving area end //////////////////////
            # return redirect(todolist)

    return render(request,'addpage.html',{})

# user todolist display page( user dashboard ) and search funtionality
@login_required(login_url="/login")
def todolist(request):

    # if method post start ///////////////////
    # for search fuctionality
    if request.method=='POST':
        search=request.POST.get('search')
        print(search)

        # search condition
        # todo_searcher=todo_db.objects.filter(email=request.user,task__icontains=search)
        # print(todo_searcher)

        # for searchvalue in todo_searcher:
        #     print(searchvalue.priority,'prioritty')


        # Filtering values from todo_db
        todo_high=todo_db.objects.filter(email=request.user,task__icontains=search,priority='High') # Fetching high priority from todo db
        todo_medium=todo_db.objects.filter(email=request.user,task__icontains=search,priority='Medium') # Fetching medium priority from todo db
        todo_normal=todo_db.objects.filter(email=request.user,task__icontains=search,priority='Normal') # Fetching normal priority from todo db
        todo_completed=todo_db.objects.filter(email=request.user,task__icontains=search,priority='Completed') # Fetching completed priority from todo db
        print(todo_high,'hhhhh')
        print(todo_medium,'mmmmm')
        print(todo_normal,'nnnnn')
        

        # id for delete purpose
        todo_delete_id=User.objects.get(username__contains=request.user)# passing user id from auth user table for delete all usertodo values
        print(todo_delete_id.id,'my id')
       

        context={'todo_delete_id':todo_delete_id,'todo_high':todo_high,'todo_medium':todo_medium,'todo_normal':todo_normal,
        'todo_completed':todo_completed}


        return render(request,'todosearch.html',context)

        # if method post end////////////////

    
    # id for delete purpose
    todo_delete_id=User.objects.get(username__contains=request.user)# passing user id from auth user table for delete all usertodo values
    print(todo_delete_id.id,'my id')

    # Filtering values from todo_db
    todo_high=todo_db.objects.filter(email__contains=request.user,priority='High') # Fetching high priority from todo db
    todo_medium=todo_db.objects.filter(email__contains=request.user,priority='Medium') # Fetching medium priority from todo db
    todo_normal=todo_db.objects.filter(email__contains=request.user,priority='Normal') # Fetching normal priority from todo db
    todo_completed=todo_db.objects.filter(email__contains=request.user,priority='Completed') # Fetching completed priority from todo db

    context={'todo_delete_id':todo_delete_id,'todo_high':todo_high,'todo_medium':todo_medium,'todo_normal':todo_normal,
    'todo_completed':todo_completed}
    return render(request,'todolistpage.html',context)

# indivdual todo's upadtion area
@login_required(login_url="/login")
def update(request,pk):
    print(pk,'my pk value')

    if request.method=='POST':
        taskdata=request.POST.get('taskdata')
        datetime=request.POST.get('datetime')
        priority=request.POST.get('priority')
        print(taskdata)
        print(datetime)
        print(priority)
        todo_edit=todo_db.objects.get(u_id=pk)
        print(todo_edit.u_id)

        if (taskdata == '' or datetime == '' or priority == ''):
            print('No value')

            context={'checker':'Please enter valid data...!',
            'taskdata':taskdata,'datetime':datetime,'priority':priority,'pk':pk}

            return render(request,'todo_editpage.html',context)

        elif ( len(taskdata)>100 ):
            print('Limit 100 Crossed')

            context={'checker':'You cross the limit of data (100 above characters reached)...!',
            'taskdata':taskdata,'datetime':datetime,'priority':priority,'pk':pk}

            return render(request,'todo_editpage.html',context)
        
        elif todo_db.objects.filter(email=request.user,task=taskdata,tasktimedate=datetime,priority=priority).exists():
            print('same data found')

            # # Filtering values from todo_db
            # todo_high=todo_db.objects.filter(email__contains=request.user,priority='High') # Fetching high priority from todo db
            # todo_medium=todo_db.objects.filter(email__contains=request.user,priority='Medium') # Fetching medium priority from todo db
            # todo_normal=todo_db.objects.filter(email__contains=request.user,priority='Normal') # Fetching normal priority from todo db

            # context={'todo_high':todo_high,'todo_medium':todo_medium,'todo_normal':todo_normal,
            # 'checker':'Same data found in your Todo List...! Please Edit or Delete Your Todo List'}
            context={'checker':'Your do not change any field values! Please change or go back to todo List',
            'taskdata':taskdata,'datetime':datetime,'priority':priority,'pk':pk}

            return render(request,'todo_editpage.html',context)# only pass context value, because render only support one dictionary value
        
        else: #update saving area
            todo_edit.task=taskdata.capitalize()
            todo_edit.tasktimedate=datetime
            todo_edit.priority=priority
            todo_edit.save()
            print('todo updated successfully')

            todo_delete_id=User.objects.get(username__contains=request.user)# passing user id from auth user table for delete all usertodo values
            print(todo_delete_id.id,'my id')
            
            # Filtering values from todo_db
            todo_high=todo_db.objects.filter(email__contains=request.user,priority='High') # Fetching high priority from todo db
            todo_medium=todo_db.objects.filter(email__contains=request.user,priority='Medium') # Fetching medium priority from todo db
            todo_normal=todo_db.objects.filter(email__contains=request.user,priority='Normal') # Fetching normal priority from todo db
            todo_completed=todo_db.objects.filter(email__contains=request.user,priority='Completed') # Fetching completed priority from todo db

            context={'todo_delete_id':todo_delete_id,'todo_high':todo_high,'todo_medium':todo_medium,'todo_normal':todo_normal,
            'todo_completed':todo_completed,'checker':'Todo updated succesfully..'}

            return render(request,'todolistpage.html',context) # only pass context value, because render only support one dictionary value

    # for the matching condition - user_id and todolist_id for hacker vulnerability-(changing the url of pk value )
    user_matcher=User.objects.get(username=request.user)
    print(user_matcher.id,'user id matcher')

    todo_edit=todo_db.objects.get(u_id=pk) # purpose are passing - matching user_id and todolist_id for hacker vulnerability(changing the url of pk value )
    print(todo_edit.login_id_id,'todo id matcher') # eg: http://127.0.0.1:8000/update/12 logined user 'id' and todo_db 'login_id' is same- ok url
    
    # main match condition                                             # - http://127.0.0.1:8000/update/40   but logined user 'id and todo_db 'login_id' is not same- not ok
    if user_matcher == todo_edit.login_id:         
        print('ids are same')
        if todo_edit.priority == 'Completed':
            print('Completed todo-- So it redirecting to todolist page')
            return redirect(todolist)
        else:
            return render(request,'todo_editpage.html',{'pk':pk,'todo_edit':todo_edit})
    else:
        print('ids are not same')
        return redirect(todolist)

    # return render(request,'todo_editpage.html',{'pk':pk,'todo_edit':todo_edit})

# individual todo's deleting view 
@login_required(login_url="/login")
def delete(request,pk):
    todo_delete=todo_db.objects.get(u_id=pk)
    print(todo_delete.u_id)
    todo_delete.delete()
    print('Todo delete successfully')

    todo_delete_id=User.objects.get(username__contains=request.user)# passing user id from auth user table for delete all usertodo values
    print(todo_delete_id.id,'my id')

    # Filtering values from todo_db
    todo_high=todo_db.objects.filter(email__contains=request.user,priority='High') # Fetching high priority from todo db
    todo_medium=todo_db.objects.filter(email__contains=request.user,priority='Medium') # Fetching medium priority from todo db
    todo_normal=todo_db.objects.filter(email__contains=request.user,priority='Normal') # Fetching normal priority from todo db
    todo_completed=todo_db.objects.filter(email__contains=request.user,priority='Completed') # Fetching completed priority from todo db

    context={'todo_delete_id':todo_delete_id,'todo_high':todo_high,'todo_medium':todo_medium,'todo_normal':todo_normal,
    'todo_completed':todo_completed,'checker':'One Todo delete succesfully..'}

    return render(request,'todolistpage.html',context) # only pass context value, because render only support one dictionary value    

# All todo's deleting view 
@login_required(login_url="/login")
def deleteall(request,pk):
    print(pk,'pk value')
    delete_all_value=todo_db.objects.filter(login_id=pk)
    delete_all_value.delete()
    print('Delete all values Succcesfully')

    return redirect (todolist)

# individual todo's changing to completed todo
@login_required(login_url="/login")
def completed(request,pk):
    todo_complete=todo_db.objects.get(email=request.user,u_id=pk)
    print(todo_complete.task)
    
    todo_complete.priority='Completed'
    todo_complete.save()
    print('priority set to completed')

    return redirect(todolist)


# logout view
def logoutpage(request):
    logout(request)

    return render(request,'index.html')


# other code - otp senting to mail
# def reset(request):
#     if request.method=='POST':
#         mobile=request.POST.get('r_mobile')
#         print(mobile)

#         otp=random.randint(1000,9999) # random password generator using random module
#         print(otp,'my otp')
        
#         send_otp(mobile,otp)
#         request.session['mobile'] = mobile
#         return redirect(otp_sender)


    
#     return render(request,'other/reset.html')

# def otp_sender(request):
#     mobile=request.session['mobile']

    
#     return render(request,'other/otp.html')