from django.shortcuts import render, redirect
from allauth.account.views import SignupView, ConfirmEmailView, PasswordResetView, PasswordResetFromKeyView
from .forms import LoginForm, SignUpForm, ChangeUserDataForm
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm


# Create your views here.




class SignUpView2(CreateView):
    template_name =  "accounts/register.html"
    def get_context_data(self, **kwargs):
        context = {}
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = SignUpForm()
        context["success"] = False
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save(request)
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            print("form is valid ")
            authenticate(username=username, password=raw_password)
            return redirect("/login/")
        

        context['form'] = form
        context["msg"] =  'Form is not valid'
        context["success"] = False
        return render(request, self.template_name, context=context)



class LoginView(TemplateView, CreateView):
    template_name = "accounts/login.html"
    def get_context_data(self, **kwargs):
        context = {}
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] =  LoginForm()
        context["msg"] =  None
        return render(request, self.template_name, context=context)
        
        
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/home/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
        context = self.get_context_data()
        context['form'] =  form
        context["msg"] =  msg
        return render(request, self.template_name, context=context)



class ChangePassword(LoginRequiredMixin,CreateView):
    template_name = 'accounts/cahnge_pass.html'
    def get_context_data(self, **kwargs):
        context={}
        form = PasswordChangeForm(self.request.user, self.request.POST or None)
        context['form']=form
        return context
    def post(self, request, *args, **kwargs):
        context=self.get_context_data()
        form = context['form']
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
        return self.render_to_response(context)




class UserSettings(LoginRequiredMixin,TemplateView,CreateView):
    template_name = 'accounts/settings.html'
    def get_context_data(self, **kwargs):
        context={}
        return context
    def get(self, request, *args, **kwargs):
        context=self.get_context_data()
        user_data_form = ChangeUserDataForm(instance=self.request.user)
        context['user_data_form'] = user_data_form
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context= self.get_context_data()
        user_data_form = ChangeUserDataForm(self.request.POST, instance=self.request.user)
        if user_data_form.is_valid():
            user_data_form.save()

        context['user_data_form'] = user_data_form
        return render(request, self.template_name, context=context)




class Dashboard(TemplateView):
    template_name = 'accounts/dashboard.html'
    def get_context_data(self, **kwargs):
        context={}
        return context
    def get(self, request, *args, **kwargs):
        context=self.get_context_data()
        return render(request, self.template_name, context=context)



