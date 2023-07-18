from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from fileServerApp.models import File
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import FileResponse
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings

# signup
def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('signup')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False
        user.save()
        activateEmail(request, user, email)
        
        messages.success(request, 'Account created successfully! ')
        return redirect('login')

    return render(request, 'registration/signup.html')

#Activate
token_generator = PasswordResetTokenGenerator()
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(str(uidb64)))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('signup')

#Actvate Email
def activateEmail(request, user, to_email):
    token_generator = PasswordResetTokenGenerator()
    uid = urlsafe_base64_encode(force_bytes(str(user.pk)))
    token = token_generator.make_token(user)
    
    mail_subject = 'Activate your user account.'
    message = render_to_string('registration/activation_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': uid,
        'token': token,
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f' Please go to you email inbox and click on received activation link to confirm and complete the registration. Check your spam folder to be sure.')
    else:
        messages.error(request, f'Problem sending confirmation email check if you typed it correctly.')
    
    
#login
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'registration/login.html')


#logout
# @login_required
def logout(request):
    auth_logout(request)
    return redirect('home')


# reset password
User = get_user_model()
def resetPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password')

        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email.')
            return redirect('reset_password')

    return render(request, 'registration/resetPassword.html')


