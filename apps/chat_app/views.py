from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.db.models import Q
# Create your views here.

def index(request):
    request.session['logged_in'] = -1
    return render(request, 'index.html')

def register(request):
    if request.POST:
        user = User.objects.filter(email = request.POST['email'])
        if not user:
            hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            new = User.objects.create(name = request.POST['name'], email = request.POST['email'], password = hashedpw)
            print('created')
            print("$$$$$$$",new.id)
            request.session['logged_in'] = new.id
            request.session['status'] = 'registered'
            return redirect('/home')
    return('/')

def login(request):
    if request.POST:
        user = User.objects.filter(email = request.POST['email'])

        if user and bcrypt.checkpw(request.POST['password'].encode('utf8'), user[0].password.encode('utf8')) :
            request.session['logged_in'] = user[0].id
            request.session['status'] = 'logged in'
            return redirect('/home')

    return redirect('/')

def home(request):
    if request.session['logged_in']:
        print(request.session['logged_in'])
        context = {'user' : User.objects.get(id = request.session['logged_in'])}

        return render(request, 'home.html', context )

    return redirect('/')

def chat(request):
    objs = User.objects.exclude(id = request.session['logged_in'] )
    print("11111111",objs)
    return render(request, "chat.html", {'users' : objs})

def write(request,id):

    # Meassges.objects.filter(Q(Message.objects.filter(sender_id= request.session['logged_in'],receiver_id = id) | Q(Message.objects.filter(sender_id= id , receiver_id = request.session['logged_in'])))
    objs = Message.objects.filter(Q(sender_id= request.session['logged_in'], receiver_id = id) | Q(sender_id= id, receiver_id = request.session['logged_in']))
    print('???????????????????',objs)

    return render(request, 'write.html',{'receiver' : User.objects.get(id = id), 'messages' : objs})

def post(request,id):
    message = Message.objects.create(content = request.POST['content'], receiver_id = id, sender_id = request.session['logged_in'])
    return redirect('/'+str(id)+'/write')

def reset(request):
    request.session.clear()
    return redirect('/')


