from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string


# Create your views here.
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = User.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
        print(pass1)

        user = User.objects.create_user(uname, email, pass1)
        user.save()
        subject = "Your new password"
        message = ""
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]

        html = render_to_string('app/pswd.html', {
            'password': pass1,

        })

        send_mail(subject, message,
                  email_from, recipient_list, html_message=html, fail_silently=False, )
        return redirect('login')

    return render(request, 'app/signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user1 = authenticate(request, username=username, password=pass1)

        if user1 is not None:
            auth.login(request, user1)
            request.session['user_status'] = 'you are successfully logged in'
            request.session['username']= user1.username
            request.session.set_expiry(3600)
            return render(request,'app/home.html',
                            {'status2':request.session['user_status'],'status':request.session['username']})
        else:
            return HttpResponse("Username or password is incorrect")

    return render(request, 'app/login.html')

def LogoutPage(request):
    # logout(request)
    request.session['user_status'] = 'logged out'
    request.session['username'] = ''
    return redirect('login')
