from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView
from .forms import SignUpForm, UserChangeForm
from .models import UserProfile


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context=context)

    def post(self, request):
        context = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context['has_error'] = True
        return render(request, self.template_name, context=context)


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'


class UpdateUserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserChangeForm
    template_name = 'user_profile_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()
        form.instance.user = user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(user=self.request.user)
