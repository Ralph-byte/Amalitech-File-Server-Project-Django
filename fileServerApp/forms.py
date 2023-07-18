from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import File


class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(label='Your Message', widget=forms.Textarea)
    
    
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('title', 'description', 'file')    

       
class EmailForm(forms.Form):
    email = forms.EmailField(label='Recipient Email')        