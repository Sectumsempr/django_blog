from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from .forms import RegisterForm, EditRegisterForm
from django.conf import settings


class AnotherLoginView(LoginView):
    template_name = 'users/login.html'


class AnotherLogoutView(LogoutView):
    template_name = 'users/logout.html'


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            about = form.cleaned_data.get('about')
            context = {'user': user, 'about': about}
            if request.FILES.get('file_field'):
                context['photo'] = request.FILES.get('file_field')
            Profile.objects.create(**context)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context=context)


class Account(View):
    def get(self, request, pk):
        user_page = User.objects.get(id=pk)
        return render(request, 'users/account.html', {'user_page': user_page})


class AccountEditFormView(View):

    def get(self, request, pk):
        if request.user.is_authenticated:
            initial = {'about': request.user.profile.about}
            if request.user.profile.photo:
                initial['file_field'] = request.user.profile.photo
            user_form = EditRegisterForm(instance=request.user, initial=initial)
        else:
            user_form = EditRegisterForm()
        return render(request, 'users/edit.html', {'user_form': user_form, 'pk': pk})

    def post(self, request, pk):
        user = User.objects.get(id=request.user.id)
        user_form = EditRegisterForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user = user_form.save()
            about = user_form.cleaned_data.get('about')
            context = {'user': user, 'about': about}
            if request.FILES.get('file_field'):
                context['photo'] = request.FILES.get('file_field')
            Profile.objects.filter(user=user).delete()
            Profile.objects.create(**context)
            return HttpResponseRedirect(f'/user/account/{pk}/')
        return render(request, 'users/edit.html', context={'user_form': user_form, 'pk': pk})
