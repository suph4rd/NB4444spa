import threading

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DeleteView
from django.views.generic.base import View
from django.views.generic.edit import FormMixin

from web import forms, utils, mixins
from B4 import models


class CustomListView(LoginRequiredMixin, generic.ListView, mixins.UserRecordMixin, View):
    pass


class CustomDetailView(mixins.UserRecordMixin, LoginRequiredMixin, generic.DetailView, View):
    pass


class CustomUpdateView(LoginRequiredMixin, mixins.IsCurrentUserMixin, generic.UpdateView, View):
    pass


class Autorization(View):

    @staticmethod
    def get(request, warning=None):
        user_form = forms.UserForm()
        warning = warning
        return render(request, 'pages/login.html', locals())

    @staticmethod
    def post(request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('web:general')
        else:
            warning = 'Неверный логин или пароль!!!'
            return Autorization.get(request=request, warning=warning)


def logout(request):
    django_logout(request)
    return redirect('web:login')


class GeneralPage(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        obj = models.Note.objects.filter(user=request.user).order_by("?").first()
        return render(request, 'pages/general.html', locals())


class DefaultDeductionsView(LoginRequiredMixin, View):
    model = models.DefaultDeductions
    form = forms.DefaultDeductionModelForm

    def get(self, request):
        qs = self.model.objects.filter(user=request.user)
        obj = qs.last() if qs.exists() \
            else self.model(user=request.user)
        form = self.form(instance=obj)
        return render(request, 'pages/default_deductions/default_deduction.html', locals())

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            obj = form.save()
        return render(request, 'pages/default_deductions/default_deduction.html', locals())


class NoteListView(LoginRequiredMixin, mixins.NoteViewMixin, FormMixin, mixins.UserRecordMixin, generic.ListView):
    template_name = "pages/note/note.html"


class NoteCreateView(LoginRequiredMixin, mixins.CKEditorErrorShowMixin, mixins.NoteViewMixin, generic.CreateView):
    template_name = "pages/note/note.html"
    check_ck_field = "text"


class NoteUpdateView(LoginRequiredMixin, mixins.IsCurrentUserMixin, mixins.CKEditorErrorShowMixin,
                     mixins.NoteViewMixin, generic.UpdateView):
    template_name = "pages/note/update_note.html"
    redirect_url = reverse_lazy('web:note')


@login_required
def get_bot_info_view(request):
    from tele_bot import main
    try:
        main.receive_records_from_telegram_bot()
    except Exception as e:
        messages.error(request, e.args[0])
    return redirect('web:note')


class TaskCreateView(LoginRequiredMixin, mixins.CKEditorErrorShowMixin, CreateView):
    model = models.Task
    check_ck_field = "description"

    def render_to_response(self, context, **response_kwargs):
        plan_id = self.request.GET.get('plan_id')
        if plan_id:
            plan = models.Plan.objects.get(pk=plan_id)
            context['plan'] = plan
            context['form'] = self.form_class(initial={"plan": plan})
        return super(TaskCreateView, self).render_to_response(context, **response_kwargs)

    def get_success_url(self):
        plan_id = self.object.plan_id
        return reverse_lazy('web:plan_detail', kwargs={'pk': plan_id}) if plan_id else super().get_success_url()


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    def dispatch(self, request, *args, **kwargs):
        answer = self._check_user(request)
        if answer:
            return answer
        return super().dispatch(request, *args, **kwargs)

    def _check_user(self, request):
        obj = self.get_object()
        if obj.plan.user_id != request.user.id:
            return redirect(reverse_lazy('web:plan_detail', kwargs={'pk': obj.plan_id}))

    def get_success_url(self):
        plan_id = self.object.plan_id
        return reverse_lazy('web:plan_detail', kwargs={'pk': plan_id}) if plan_id else super().get_success_url()


class PlanCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "pages/plan/create.html"
    form_class = forms.get_custom_model_form(models.Plan, fields_list=['name', 'user'])

    def get_initial(self):
        return {"user": self.request.user}


@login_required
def create_today_plan_task_view(request):
    utils.PlanTask.create_today_plan(request.user.id)
    return redirect('web:plan_list')

