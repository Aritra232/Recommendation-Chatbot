from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from .bot import get_bot_response


#from django.http import HttpResponse
from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from chatbot.models import userinfo
from django.contrib import messages
from django.template import loader
from django.db.models import Count
from django.core.exceptions import ValidationError

from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='login')
def home(request):
    return render(request, 'chatbot/chat.html')

def loginpage(request):

    if request.method == "POST" :
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')

        user = authenticate(request,username=username,password=pass1)

        if user is not None:
            mydata = userinfo(username=username)
            mydata.save()
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Your username or password is not valid!!!")
        
    return render(request,"chatbot/login.html")


def signuppage(request):
    if request.method == "POST":
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists!")
            
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists!")
        
        if pass1!=pass2:
            return HttpResponse("Your password and confirm password both are not same!!!")
        else:
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')

        

    return render(request,"chatbot/sign.html")

'''def homey(request):
    return render(request,"homepage1.html")'''

def logoutpage(request):
    logout(request)
    return redirect('login')



# def get_response(request):
#     if request.method == 'POST':
#         # Capture the input text field
#         query_text = request.POST.get('query_sent')

#         # Validate for empty input (optional, but recommended for user experience)
#         if not query_text:
#             return HttpResponseBadRequest('Please enter a query.')
        
#         bot_response = get_bot_response(query_text)

#         # Render the HTML page with the processed text
#         context = {'Query': query_text , 'Response': bot_response}
#         # print("--------", context, "------------------")
#         return render(request, 'chatbot/response.html', context)
#     else:
#         # Handle non-POST requests (optional, but good practice)
#         return HttpResponseBadRequest('Invalid request method. Please use POST.')
def get_response(request):
    if request.method == 'POST':
        query_text = request.POST.get('query_sent')
        if not query_text:
            return HttpResponseBadRequest('Please enter a query.')
        bot_response = get_bot_response(query_text)
        return JsonResponse({'Response': bot_response})
    else:
        return HttpResponseBadRequest('Invalid request method. Please use POST.')
