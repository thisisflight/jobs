from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from skills.forms import TagForm, TagValueForm
from skills.models import TagValue, UserTagValue
from utils.process_values import get_values_data
from .forms import SignInForm, SignUpForm

User = get_user_model()


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        """Если пользователь залогинен,
        ему незачем заходить на эту страницу"""
        if request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        result = super().form_valid(form)
        username = form.cleaned_data['username']
        user = User.objects.get(username=username)
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        login(self.request, user=user)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание аккаунта'
        return context


class SignInView(LoginView):
    form_class = SignInForm
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        """Если пользователь залогинен,
        ему незачем заходить на эту страницу"""
        if request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход в аккаунт'
        return context


@require_POST
def check_username(request):
    """Проверка вводимого при регистрации пользователя username посредством htmx"""
    username = request.POST.get('username')
    if not len(username):
        return HttpResponse("")
    if User.objects.filter(username=username).exists():
        return HttpResponse(
            "<div style='color: red'>Такое имя пользователя уже существует</div>"
        )
    return HttpResponse(
        "<div style='color: green'>Такое имя пользователя доступно</div>"
    )


@login_required
def profile_view(request):
    # Страница профиля пользователя, доступна только ему
    if request.method == 'POST':
        if 'first_form' in request.POST:
            tag = TagForm(request.POST)
            if tag.is_valid():
                tag.save()
                return redirect('accounts:profile')
        elif 'second_form' in request.POST:
            value = TagValueForm(request.POST)
            if value.is_valid():
                value.save()
                return redirect('accounts:profile')
    tag_form = TagForm()
    tag_value_form = TagValueForm()
    tag_values = TagValue.objects.select_related('tag')
    tag_values_to_add = tag_values.exclude(user__in=[request.user.pk])
    users_tag_values = tag_values.filter(user__in=[request.user.pk])
    user_data = get_values_data(users_tag_values)
    context = {
        'tag_form': tag_form,
        'tag_value_form': tag_value_form,
        'values_to_add': tag_values_to_add,
        'users_tag_values': users_tag_values,
        'user_data': user_data
    }
    return render(request, 'accounts/profile.html', context)


@login_required
@require_POST
def add_tag(request, pk):
    """Добавление навыка"""
    user = request.user
    tag_value = TagValue.objects.get(pk=pk)
    UserTagValue.objects.create(user=user, tag_value=tag_value)
    return redirect('accounts:profile')


@login_required
@require_POST
def delete_tag(request, pk):
    """Удаление навыка"""
    user = request.user
    tag_value = TagValue.objects.get(pk=pk)
    user_tag_value = UserTagValue.objects.filter(user=user, tag_value=tag_value)
    user_tag_value.delete()
    return redirect('accounts:profile')
