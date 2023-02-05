from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,logout,login
from users.forms import LoginForm,RegisterForm
from django.contrib.auth.models import User
from django.views.generic import CreateView,RedirectView,TemplateView
# Create your views here.

class LoginView(TemplateView):

    def get(self,request,**kwargs):
        context = {
            'form': LoginForm
        }
        return render(request, self.template_name, context=context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        form = LoginForm(data=data)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'))

            if user:
                login(request, user)
                return redirect('/products')
            else:
                form.add_error('username', 'try again')

        return render(request, 'users/login.html', context={
            'form': form
        })

class LogoutView(RedirectView):
    def get(self,request,*args,**kwargs):
     logout(request)
     return redirect('/products')



class RegisterView(CreateView):

    def get(self,request,**kwargs):
        context = {
            'form': RegisterForm
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            password1, password2 = form.cleaned_data.get('password1'), form.cleaned_data.get('password2')
            if password1 == password2:
                User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password1')
                )
                return redirect('/users/login/')
            else:
                form.add_error('password1', 'try again')

        return render(request, self.template_name, context={
            'form': form
        })

