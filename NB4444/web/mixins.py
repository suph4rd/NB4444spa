from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from B4 import models
from web import forms


class NoteViewMixin:
    form_class = forms.NoteModelForm
    model = models.Note
    queryset = None
    success_url = reverse_lazy("web:note")

    def get_initial(self):
        self.initial = {"user": self.request.user}
        return super().get_initial()


class UserRecordMixin:
    model = None
    queryset = None

    def dispatch(self, request, *args, **kwargs):
        if self.model and not self.queryset:
            self.queryset = self.model.objects.all()
        if self.queryset and hasattr(self.model, 'user') \
                and request.user.is_authenticated and not request.user.is_superuser:
            self.queryset = self.queryset.filter(user=request.user)
        return super().dispatch(request, *args, **kwargs)


class IsCurrentUserMixin:
    redirect_url: str = None

    def dispatch(self, request, *args, **kwargs):
        answer = self._check_user(request)
        if answer:
            return answer
        return super().dispatch(request, *args, **kwargs)

    def _check_user(self, request):
        obj = self.get_object()
        if obj.user_id != request.user.id:
            return redirect(self.redirect_url)


class CKEditorErrorShowMixin:
    check_ck_field: str = None

    def form_invalid(self, form):
        if self.check_ck_field in form.errors:
            messages.error(self.request, f"{self.check_ck_field}: {form.errors[self.check_ck_field]}")
        return redirect(reverse_lazy('web:note'))
