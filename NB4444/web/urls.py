"""NB4444 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, reverse_lazy
from django.views import generic

from B4 import models
from . import forms, utils, views

app_name = 'b4'
urlpatterns = [
    path('', views.GeneralPage.as_view(), name='general'),
    path('accounts/login/', views.Autorization.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),

    path('default-deductions/', views.DefaultDeductionsView.as_view(), name='default_deductions'),
    path('note/', views.NoteListView.as_view(), name='note'),
    path('note/create', views.NoteCreateView.as_view(), name='note_create'),
    path('note/update/<int:pk>/', views.NoteUpdateView.as_view(), name='note_update'),
    path(
        'note/delete/<int:pk>/',
        utils.made_login_required_generic_class(generic.DeleteView).as_view(
            model=models.Note,
            template_name='pages/note/delete.html',
            success_url=reverse_lazy('web:note')
        ),
        name='note_delete'
    ),
    path(
        'plan/',
        views.CustomListView.as_view(
            model=models.Plan,
            template_name="pages/plan/list.html"
        ),
        name='plan_list'
    ),
    path(
        'plan/<int:pk>/',
        views.CustomDetailView.as_view(
            model=models.Plan,
            template_name="pages/plan/detail.html"
        ),
        name='plan_detail'
    ),
    path(
        'plan/create/',
        views.PlanCreateView.as_view(),
        name='plan_create'
    ),
    path(
        'plan/update/<int:pk>/',
        views.CustomUpdateView.as_view(
            model=models.Plan,
            redirect_url=reverse_lazy('web:plan_list'),
            form_class=forms.get_custom_model_form(models.Plan, fields_list=['name', 'user']),
            template_name="pages/plan/update.html"
        ),
        name='plan_update'
    ),
    path(
        'plan/delete/<int:pk>/',
        utils.made_login_required_generic_class(generic.DeleteView).as_view(
            model=models.Plan,
            template_name='pages/plan/delete.html',
            success_url=reverse_lazy('web:plan_list')
        ),
        name='plan_delete'
    ),
    path('plan/create-today-plan/', views.create_today_plan_task_view, name='plan_today_create'),
    path(
        'plan/task/create/',
        views.TaskCreateView.as_view(
            model=models.Task,
            # form_class=forms.get_custom_model_form(models.Task),
            form_class=forms.TaskModelForm,
            template_name="pages/task/create.html"
        ),
        name='task_create'
    ),
    path(
        'plan/task/update/<int:pk>/',
        utils.made_login_required_generic_class(generic.UpdateView).as_view(
            model=models.Task,
            form_class=forms.TaskModelForm,
            template_name="pages/task/update.html"
        ),
        name='task_update'
    ),
    path(
        'plan/task/delete/<int:pk>/',
        views.TaskDeleteView.as_view(
            model=models.Task,
            template_name='pages/task/delete.html',
        ),
        name='task_delete'
    ),
    path('bot-response/', views.get_bot_info_view, name='bot_response'),
    path(
        'user-create/',
        generic.CreateView.as_view(
            model=models.User,
            form_class=forms.UserModelForm,
            template_name="pages/registration/create_user.html",
            success_url=reverse_lazy("web:general")
        ),
        name='user_create'
    ),
]
