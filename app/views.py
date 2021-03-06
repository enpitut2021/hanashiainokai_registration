from json import encoder
from django.contrib.auth.models import User

from .forms import BS4ScheduleForm_edit, RegistrationForm, LoginForm

from django.db.models import Q

from django.contrib.auth import authenticate, login, logout as django_logout
from django.core.paginator import Paginator
from django.core.validators import ValidationError

import base64

from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework.views import APIView

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

import datetime
from django.shortcuts import redirect, render
from django.views import generic
from .forms import BS4ScheduleForm, SimpleScheduleForm
from .models import Discord_User, Schedule
from . import mixins

from operator import attrgetter

def login_user(request):
    params = {
        'login_form': LoginForm(),
    }
    if request.method == 'POST':
        params['login_form'] = LoginForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        username = request.POST['username']
        password = request.POST['password']
        username2 = base64.b64encode(username.encode())
        password2 = base64.b64encode(password.encode())
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            params['login_form'].add_error(None, "ユーザ名またはパスワードが異なります")
            return render(request, 'app/login.html', params)
    return render(request, 'app/login.html', params)
    #アカウントとパスワードが合致したら、その人専用の投稿画面に遷移する
    #アカウントとパスワードが合致しなかったら、エラーメッセージ付きのログイン画面に遷移する

def registration_user(request):
    params = {
        'registration_form': RegistrationForm(),
    }
    if request.method == 'POST':
        params['registration_form'] = RegistrationForm(request.POST)
        if request.POST['email'].rsplit('@',1)[1] != 's.tsukuba.ac.jp' and request.POST['email'].rsplit('@',1)[1] != 'alumuni.tsukuba.ac.jp':
            params['registration_form'].add_error('email', "筑波大学のemailアカウントを使用してください。\n\n使用できるメールアドレス: sアド, alumuni")
        if params['registration_form'].has_error('email'):
            return render(request, 'app/registration.html', params)
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        return redirect('login')
    return render(request, 'app/registration.html', params)

def index(request):
    # username_index = username.split("'")
    # username = username_index[1]
    # username3 = base64.b64decode(username).decode()

    # password_index = password.split("'")
    # password = password_index[1]
    # password3 = base64.b64decode(password).decode()

    # user = authenticate(username=username3, password=password3)
    # params = {
    #     'user': user,
    # }
    # if user is None:
    #     return redirect('login')
    return render(request, 'app/index.html')

def logout(request):
    django_logout(request)
    return render(request, 'app/logout.html')

""" @require_POST """
class delete_schedule(DeleteView):
    template_name = 'app/delete.html'
    model = Schedule

    date = datetime.date.today()

    def get_success_url(self):
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        date = schedule.date
        return reverse('mycalendar', kwargs={'year':date.year, 'month':date.month, 'day':date.day})
    
class Join(CreateView):
    template_name = 'app/join.html'
    model = Discord_User
    fields = ['discord_name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        context['schedule'] = schedule
        print(context)
        return context    
 
    def get_form(self):
        form = super(Join, self).get_form()
        form.fields['discord_name'].label = 'あなたのDiscordの名前 (例: name#0000)'
        return form
    
    def form_valid(self, form):
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        instance = form.save()
        schedule.participants.add(instance)
        return super(Join,self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('detail', kwargs={'pk':pk})

class Detail(DetailView):
    template_name = 'app/detail.html'
    model = Schedule

class Update(UpdateView):
    template_name = 'app/edit.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm_edit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        context['schedule'] = schedule
        context['edit_form'] = BS4ScheduleForm_edit
        return context
 
    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        schedule = form.save(commit=False)
        schedule.save()
        return redirect('detail', pk=schedule.id)

class MonthCalendar(mixins.MonthCalendarMixin, generic.TemplateView):
    """月間カレンダーを表示するビュー"""
    template_name = 'app/month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""
    template_name = 'app/month_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class MyCalendar(mixins.MonthCalendarMixin, mixins.WeekWithScheduleMixin, mixins.DayWithScheduleMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'app/mycalendar.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        day_calendar_context = self.get_day_calendar()
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(day_calendar_context)
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.save()
        return redirect('mycalendar', year=date.year, month=date.month, day=date.day)

class ToBot(mixins.MonthCalendarMixin, mixins.DayWithScheduleMixin, generic.CreateView):
    template_name = 'app/tobot.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        day_calendar_context = self.get_day_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(day_calendar_context)
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):
        pass

class MonthWithFormsCalendar(mixins.MonthWithFormsMixin, generic.View):
    """フォーム付きの月間カレンダーを表示するビュー"""
    template_name = 'app/month_with_forms.html'
    model = Schedule
    date_field = 'date'
    form_class = SimpleScheduleForm

    def get(self, request, **kwargs):
        context = self.get_month_calendar()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_month_calendar()
        formset = context['month_formset']
        if formset.is_valid():
            formset.save()
            return redirect('app:month_with_forms')

        return render(request, self.template_name, context)

class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""
    template_name = 'app/month_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class ScheduleList(ListView):
    model = Schedule
