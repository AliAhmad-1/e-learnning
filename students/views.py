from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView,ListView,DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from courses.models import Course

# Create your views here.


class StudentRegestrationView(CreateView):
    template_name='students/registration.html'
    form_class=UserCreationForm
    success_url=reverse_lazy('student_course_list')

    def form_valid(self, form):
        form=form.cleaned_data
        user=authenticate(username=form['username'],password=form['password1'])
        login(self.request,user)
        return super().form_valid(form)
    


class StudentEnrollCourseView(LoginRequiredMixin,FormView):
    course=None
    form_class=CourseEnrollForm
    def form_valid(self, form):
        self.course=form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail' ,args=[self.course.id])
    

class  StudentCourseListView(LoginRequiredMixin,ListView):
    model=Course
    template_name='courses/student_course_list.html'

    def get_queryset(self):
        qs=super().get_queryset()
        qs.filter(students__in=[self.request.user])
        return qs
    

class StudentCourseDetailView(DetailView):
    model=Course
    template_name='courses/student_course_detail.html'

    def get_queryset(self):
        qs=super().get_queryset()
        qs.filter(students__in=[self.request.user])
        return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course=self.get_object()
        if 'module_id' in self.kwargs:
            context["module"] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module']=course.modules.all()[0]
        return context
    
    