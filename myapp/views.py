
from django.http import HttpResponse, response, HttpResponseRedirect
from django.urls import reverse
from myapp.forms import TopicForm, InterestForm,RegistrationForm
from myapp.models import Author, Book, Course, Topic,Student
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect,render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'myapp/index.html'

    def get_queryset(self):
        return Course.objects.all()

# def index(request):
#     courselist=Course.objects.all().order_by('title')[:10]
#     return render(request,'myapp/index.html',{'courselist':courselist})

def about(request):
    return render(request,'myapp/about.html')

class DetailView(generic.DetailView):
    model = Course
    template_name = 'myapp/detail.html'

# def detail(request,course_no):
#     courseno = get_object_or_404(Course, pk=course_no)
#     return render(request, 'myapp/detail.html', {'courseno': courseno})
def viewProfile(request):
    args = {'user':request.user}
    return render(request,'myapp/profile.html',args)

def topics(request):
    topiclist = Topic.objects.all()
    return render(request, 'myapp/topics.html', {'topiclist':   topiclist})

def addtopic(request):
    topiclist = Topic.objects.all()
    if request.method=='POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.num_responses=1
            topic.save()
            return HttpResponseRedirect(reverse('myapp:topics'))
    else:
        form=TopicForm()
    return render(request, 'myapp/addtopic.html', {'form':form, 'topiclist':topiclist})

def topicdetail(request, topic_id):
    global form
    topic_id = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        interestForm = InterestForm(request.POST)
        if interestForm.is_valid():
            if interestForm.cleaned_data['interested'] == '1':
                form = TopicForm(instance=topicdetail)
                topic = form.save(commit=False)
                topic.num_responses = topic.num_responses + 1
                topic.avg_age = (topic.avg_age * (topic.num_responses) + interestForm.cleaned_data['age']) / (
                topic.num_responses + 1)
                topic.save()
                return HttpResponseRedirect(reverse('myapp:topics'))
            else:
                return HttpResponseRedirect(reverse('myapp:topics'))
    else:
        form = InterestForm()
    return render(request, 'myapp/topicdetail.html', {'form': form, 'topicdetail': topic_id})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/myapp')
    else:
        form = RegistrationForm()
        return render(request, 'myapp/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp/templates/myapp/mycourse.html')) #
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/templates/registration/login.html')

@login_required
def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('/myapp/templates/registration/login.html')))

# class CoursebyUser(LoginRequiredMixin,generic.Listview):
#     model = Course
#     template = 'myapp/mycourse.html'
#     paginate_by = 10
#
#     def get_queryset(self):
#         return Course.objects.filter(student=self.request.user)

def mycourse(request):
    studententry = len(Student.objects.filter(username=request.user.username))
    if studententry == 1:
        stud = Student.objects.get(username=request.user.username)
        courses = stud.course_set.all()
        return render(request,'myapp/mycourse.html',{'courses':courses,'requser':request.user})
    else:
        return render(request,'myapp/mycourse.html',{'flag':1,'requser':request.user})

