from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myapp.models import Topic,Student


class TopicForm(forms.ModelForm):
    class Meta:
        model=Topic
        fields = ['subject', 'intro_course', 'time', 'avg_age']
        widgets = {'time': forms.RadioSelect(), }
        labels = {'time':u'Preferred Time','avg_age':u'What is your age?','intro_course':u'This should be an introductory level course'}

class InterestForm(forms.Form):
    interested = forms.TypedChoiceField(widget=forms.RadioSelect(),coerce=int,choices=((1,"Yes"),(0,"No")))
    age = forms.IntegerField(initial= 20)
    comments = forms.CharField(widget=forms.Textarea(),label='Additional Comments',required=False)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Student
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','age','city','province')
        widgets = {'province': forms.RadioSelect(),}

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.age = self.cleaned_data['age']
        user.city = self.cleaned_data['city']
        user.province = self.cleaned_data['province']

        if commit:
            user.save()

        return user