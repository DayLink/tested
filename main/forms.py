# -*- coding: <encoding name> -*-

from django.forms import ModelForm
from main.models import Comment
from django import forms
from models import MyUser
from tinymce.widgets import TinyMCE
from django.conf import settings
from django.forms.extras.widgets import SelectDateWidget

class CalendarWidget(forms.TextInput):

    class Media:
        js = ('/admin/jsi18n/',
              settings.ADMIN_MEDIA_PREFIX + 'js/core.js',
              settings.ADMIN_MEDIA_PREFIX + "js/calendar.js",
              settings.ADMIN_MEDIA_PREFIX + "js/admin/DateTimeShortcuts.js")
        css = {
            'all': (
                settings.ADMIN_MEDIA_PREFIX + 'css/forms.css',
                settings.ADMIN_MEDIA_PREFIX + 'css/base.css',
                settings.ADMIN_MEDIA_PREFIX + 'css/widgets.css',)
        }

    def __init__(self, attrs={}):
        super(CalendarWidget, self).__init__(attrs={'class': 'vDateField', 'size': '10'})

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'content']

class RegistrationForm(forms.Form):
    username = forms.CharField(label=(u'User Name'))
    name = forms.CharField(label=(u'Name'))
    email = forms.EmailField(label=(u'Email'))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))
    date_of_birth = forms.DateField(widget=SelectDateWidget, label=(u'Date'))
    gender = forms.ChoiceField(choices=(('M','Male'),('F','Female')), label=(u'Gender'))

    def clean_username(self):
        data = self.cleaned_data['username']
        try:
            MyUser.objects.get(username=data)
        except:
            pass
        else:
            raise forms.ValidationError("This user already exists")
        return data

    def clean(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password and password != password1:
            raise forms.ValidationError("Passwords don't mach")

        return self.cleaned_data

class ProfileForm(forms.Form):
    username = forms.CharField(label=(u'User Name'), widget=TinyMCE(attrs={'cols': 40, 'rows': 1}))

class LoginForm(forms.Form):
    username = forms.CharField(label=(u'User Name'))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))