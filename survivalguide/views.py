from __future__ import absolute_import

from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from braces import views

from .forms import RegistrationForm
from .forms import LoginForm

from talks.models import TalkList


class HomePageView(generic.TemplateView):
    template_name = 'home.html'

class SignUpView(views.AnonymousRequiredMixin,
        views.FormValidMessageMixin,generic.CreateView):
    form_class = RegistrationForm
    model = User
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.form_valid_message = 'Account successfully created.'
        resp = super(SignUpView, self).form_valid(form)
        TalkList.objects.create(user=self.object, name='To Attend')
        return resp

class LoginView(views.AnonymousRequiredMixin,
        views.FormMessagesMixin,generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/login.html'
    form_invalid_message = ''

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            self.form_valid_message = 'Login successful.'
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)

class LogOutView(generic.RedirectView, views.LoginRequiredMixin,
        views.MessageMixin):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        self.messages.success("You've been logged out. Come back soon!")
        return super(LogOutView, self).get(request, *args, **kwargs)



