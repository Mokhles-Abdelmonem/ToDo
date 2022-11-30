from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, View
from . forms import AddTaskForm
from .models import ToDoDate , TaskGroup, Task
import datetime
import calendar
from django.contrib.auth.decorators import login_required




# Create your views here.


class Home(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/home.html'
    def get_context_data(self,*args, **kwargs):
        day_id = self.request.GET.get('day')
        context={}
        form = AddTaskForm(self.request.POST or None)
        context["form"] = form
        tododata = ToDoDate.objects.filter(user=self.request.user,date=datetime.date.today())
        tasks_list = []
        if tododata.exists():
            day_obj = tododata[0]
        if day_id:
            day_obj = ToDoDate.objects.get(id=int(day_id))
        groups = TaskGroup.objects.filter(date=day_obj)
        for group in groups:
            tasks = Task.objects.filter(group=group)
            tasks_list.append({
                "title" : group.title,
                "id" : group.id,
                "tasks" : tasks,
                })
        old_days = ToDoDate.objects.filter(user=self.request.user).exclude(date=datetime.date.today())
        context["day_obj"] = day_obj
        context["old_days"] = old_days
        context["groups"] = tasks_list
        return context
    def get(self, request, *args, **kwargs):
        context=self.get_context_data()
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context=self.get_context_data()
        form = context["form"]

        if form.is_valid():
            group_name  = form.cleaned_data.get("group_name")
            day_id = self.request.GET.get('day')
            if day_id:
                date_obj = ToDoDate.objects.get(id=int(day_id))
                print("\n date_obj \n")
                print(date_obj)
            else:
                todo_date = ToDoDate.objects.get_or_create(
                    user=request.user,
                    date=datetime.date.today(),
                )
                date_obj = todo_date[0]

            task_group = TaskGroup.objects.get_or_create(
                date=date_obj ,
                title=group_name,
            )

            instance = form.save(commit=False)
            instance.group = task_group[0]
            instance.save()
            return redirect("home_dashboard")
        return render(request, self.template_name, context=context)



@login_required(login_url='login')
def deletetask(request,  id):
    user = request.user
    task_obj = Task.objects.get(id=id)
    if user == task_obj.group.date.user :
        task_obj.delete()
    return redirect('home_dashboard')

@login_required(login_url='login')
def deleteSelected(request):
    user = request.user
    tasks_ids = request.POST.getlist('ids[]')
    for id in tasks_ids:
        task_obj = Task.objects.get(id=id)
        if user == task_obj.group.date.user:
            task_obj.delete()
    return redirect('home_dashboard')

