import logging
import socket
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import File
from django.contrib.auth.tokens import default_token_generator
import mimetypes
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import FileResponse
from django.core.mail import EmailMessage
from .forms import ContactForm, EmailForm, FileUploadForm
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')

#Feed
def feed(request):
    files = File.objects.all()
    return render(request, 'feed.html', {'files': files})

#Search
def search(request):
    query = request.GET.get('q')
    if query:
        files = File.objects.filter(title__icontains=query)
    else:
        files = File.objects.all()
    return render(request, 'search.html', {'files': files, 'query': query})

#Preview
@login_required
def preview(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    return render(request, 'preview.html', {'file': file})


#Download
def download_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    file.download_count += 1
    file.save()
    return FileResponse(open(file.file.path, 'rb'), content_type='application/octet-stream')


#Send Email

logger = logging.getLogger(__name__)

def send_email(request, file_id):
    file = File.objects.get(pk=file_id)
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            try:
                email_message = EmailMessage(
                    subject='File Sharing: File Download',
                    body=f'You received a file titled "{file.title}" from File Sharing Platform. Please find it attached.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )

                with open(file.file.path, 'rb') as attachment:
                    content_type, _ = mimetypes.guess_type(file.file.path)
                    email_message.attach(file.title, attachment.read(), content_type)

                email_message.send()
                logger.info('Email sent successfully')

                file.email_count += 1
                file.save()

                return redirect('feed')

            except socket.gaierror as e:
                logger.error(f'getaddrinfo failed: {e}')
                error_message = 'Failed to send the email. Please try again later.'
                return render(request, 'send_email.html', {'form': form, 'file': file, 'error_message': error_message})

            except Exception as e:
                logger.error(f'Error sending email: {e}')
                error_message = 'An unexpected error occurred. Please contact the administrator.'
                return render(request, 'send_email.html', {'form': form, 'file': file, 'error_message': error_message})

    else:
        form = EmailForm()

    return render(request, 'send_email.html', {'form': form, 'file': file})

#Upload
#@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.uploaded_by = request.user
            file.save()
            messages.success(request, 'File uploaded successfully.')
            return redirect('feed')
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})


#Contact
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            
            # Process the form data here
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # send an email
            send_mail(
                'Contact Form Submission',
                f'Name: {name}\nEmail: {email}\nMessage: {message}',
                'dumakorandrin@gmail.com',  # email address
                ['raphael.dumakor@amalitech.org'],  
                fail_silently=False,
            )
            # Redirect or show a success message
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


