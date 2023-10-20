from django.test import Client, TestCase
from django.urls import reverse

from B4 import models


class B4URLCommonMixin:
    custom_client = None

    def test_url_b4_general(self):
        url = "b4:general"
        response = self.custom_client.get(reverse(url))
        self.assertEqual(response.status_code, 200)

    def test_url_b4_login(self):
        url = "b4:login"
        response = self.custom_client.get(reverse(url))
        self.assertEqual(response.status_code, 200)

    def test_url_b4_logout(self):
        url = "b4:logout"
        response = self.custom_client.get(reverse(url))
        self.assertEqual(response.status_code, 302)

    def test_url_b4_default_deductions(self):
        url = "b4:default_deductions"
        response = self.custom_client.get(reverse(url))
        self.assertEqual(response.status_code, 200)

    def test_url_b4_note(self):
        url = "b4:note"
        response = self.custom_client.get(reverse(url))
        self.assertEqual(response.status_code, 200)

    def test_url_b4_plan_list(self):
        url = "b4:plan_list"
        response = self.custom_client.get(reverse(url))
        self.assertEqual(response.status_code, 200)

    def test_url_b4_plan_detail(self):
        url = "b4:plan_detail"
        obj = models.Plan.objects.last()
        self.assertEqual(bool(obj), True)
        pk = obj.pk
        response = self.custom_client.get(reverse(url, kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 200)

    def test_url_b4_plan_create(self):
        url = "b4:plan_create"
        response = self.custom_client.get(reverse(url))
        self.assertEqual(response.status_code, 200)

    def test_url_b4_plan_update(self):
        url = "b4:plan_update"
        obj = models.Plan.objects.last()
        self.assertEqual(bool(obj), True)
        pk = obj.pk
        response = self.custom_client.get(reverse(url, kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 200)

    def test_url_b4_plan_delete(self):
        url = "b4:plan_delete"
        obj = models.Plan.objects.last()
        self.assertEqual(bool(obj), True)
        pk = obj.pk
        response = self.custom_client.get(reverse(url, kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 200)

    def test_url_b4_plan_today_create(self):
        url = "b4:plan_today_create"
        response = self.custom_client.get(reverse(url))
        self.assertEqual(response.status_code, 302)

    def test_url_b4_task_create(self):
        url = "b4:task_create"
        response = self.custom_client.get(reverse(url))
        self.assertEqual(response.status_code, 200)

    def test_url_b4_task_update(self):
        url = "b4:task_update"
        obj = models.Task.objects.last()
        self.assertEqual(bool(obj), True)
        pk = obj.pk
        response = self.custom_client.get(reverse(url, kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 200)

    def test_url_b4_task_delete(self):
        url = "b4:task_delete"
        obj = models.Task.objects.last()
        self.assertEqual(bool(obj), True)
        pk = obj.pk
        response = self.custom_client.get(reverse(url, kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 200)


class B4URLTestsSuperuser(B4URLCommonMixin, TestCase):
    custom_variables: dict = None

    def setUp(self) -> None:
        client = Client()
        self.custom_variables['user'] = models.User.objects.create_superuser(
            email='root@root.root',
            username='root',
            password='12345TestCase'
        )
        client.login(username='root', password='12345TestCase')
        self.custom_client = client

        # plans
        self.custom_variables['plan'] = models.Plan.objects.create(user=self.custom_variables.get("user"), name="plan")
        # section
        self.custom_variables['section'] = models.Section.objects.create(name="section", is_active=True)
        # tasks
        self.custom_variables['task'] = models.Task.objects.create(
            plan=self.custom_variables.get("plan"),
            section=self.custom_variables.get("section"),
            description="",
            is_ready=False
        )


class B4URLTestsUser(B4URLCommonMixin, TestCase):
    custom_variables: dict = None

    def setUp(self) -> None:
        client = Client()
        self.custom_variables = {'user': models.User.objects.create_user(
            email='user@user.user',
            username='user',
            password='12345TestCase'
        )}
        client.login(username='user', password='12345TestCase')
        self.custom_client = client

        # plans
        self.custom_variables['plan'] = models.Plan.objects.create(user=self.custom_variables.get("user"), name="plan_user")
        # section
        self.custom_variables['section'] = models.Section.objects.create(name="section_user", is_active=True)
        # tasks
        self.custom_variables['task'] = models.Task.objects.create(
            plan=self.custom_variables.get("plan"),
            section=self.custom_variables.get("section"),
            description="",
            is_ready=False
        )

