
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from .mixins import FieldsMixins, FormValidMixins, AuthorAccessMixins, SuperuserAccessMixins, AuthorsAccessMixins
from .models import User
from .forms import ProfileForm, SignupForm
from blog.models import Article

# Register
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


# Create your views here.


class ArticleListView(AuthorsAccessMixins, ListView):
    template_name = "registration/home.html"
    context_object_name = 'articles'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreateView(AuthorsAccessMixins, FormValidMixins, FieldsMixins, CreateView):
    model = Article
    template_name = "registration/article_create_update.html"
    

class ArticleUpdateView(AuthorAccessMixins, FormValidMixins, FieldsMixins, UpdateView):  # we dont need to
    # 'LoginRequiredMixin' beacase in 'AuthorAccessMixins' we check author
    model = Article
    template_name = "registration/article_create_update.html"


class ArticleDeleteView(SuperuserAccessMixins, DeleteView):
    model = Article
    template_name = "registration/article_delete.html"
    success_url = reverse_lazy("account:home")
    context_object_name = "article"


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "registration/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("account:profile")

    def get_object(self, **kwargs):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update(
            {'user': self.request.user}
        )
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_author:
            return reverse_lazy("account:home")
        else:
            return reverse_lazy("account:profile")


class Register(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی حساب کاربری'
        message = render_to_string('registration/active_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return HttpResponse(
            'لینک فعال سازی به ایمیل شما ارسال شد. برای تایید حساب کاربری بر روی لینک ارسال شده کلیک کنید.')


# def signup(request):
#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#
#             current_site = get_current_site(request)
#             mail_subject = 'فعال سازی حساب کاربری'
#             message = render_to_string('registration/active_account.html' , {
#                 'user' : user,
#                 'domain' : current_site.domain,
#                 'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token' : account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(mail_subject , message , to=[to_email])
#             email.send()
#
#             return HttpResponse('لینک فعال سازی به ایمیل شما ارسال شد. برای تایید حساب کاربری بر روی لینک ارسال شده کلیک کنید.')
#     else:
#         form = SignupForm()
#     return render(request , 'signup.html' , {'form' : form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # if we want to login user
        # login(request , user)
        return HttpResponse('حساب کاربری شما با موفقیت فعال شد.')
    else:
        return HttpResponse('لینک فعال سازی منقضی شده است.')
