import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

NULL_BLANK = {
    "null": True,
    "blank": True
}


class SafeManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_delete=False)


class AbstractSafeModel(models.Model):
    is_delete = models.BooleanField("Удалено", default=False)
    delete_datetime = models.DateTimeField("Дата удаления", **NULL_BLANK)
    objects = SafeManager()
    all_objects = models.Manager()

    @classmethod
    def get_admin_manager(cls):
        return cls.all_objects

    def delete(self, using=None, keep_parents=False, force=False):
        if force:
            return super().delete(using=None, keep_parents=False)
        self.is_delete = True
        self.delete_datetime = datetime.datetime.now()
        self.save()

    class Meta:
        abstract = True


class TimeModel(models.Model):
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, **NULL_BLANK)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True, **NULL_BLANK)

    class Meta:
        abstract = True


class User(AbstractUser):
    class Meta:
        db_table = "auth_user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


User.get_full_name.short_description = "Фамилия Имя"


class DefaultDeductions(TimeModel, AbstractSafeModel):
    house = models.DecimalField('Жильё', default=0, max_digits=10, decimal_places=2)
    travel = models.DecimalField('Проезд', default=0, max_digits=10, decimal_places=2)
    phone = models.DecimalField('Телефон', default=0, max_digits=10, decimal_places=2)
    food = models.DecimalField('Еда', default=0, max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Стандартные вычеты'
        verbose_name_plural = 'Стандартные вычеты'

    def __str__(self):
        return f"{self.id} {self.created_at}"

    @property
    def total(self):
        return f"{self.house + self.travel + self.phone + self.food}"


class Note(TimeModel, AbstractSafeModel):
    text = models.TextField('Текст', **NULL_BLANK)
    image = models.ImageField('Фотоверсия', upload_to="foto/%Y/%m/%d", **NULL_BLANK)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name='notes')

    class Meta:
        verbose_name = 'Заметки'
        verbose_name_plural = 'Заметки'
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f"{self.pk} {self.created_at}"


class Plan(TimeModel, AbstractSafeModel):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name='plans')
    name = models.CharField('Название плана', max_length=255)

    class Meta:
        verbose_name = 'План'
        verbose_name_plural = 'Планы'
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f"{self.id} {self.name}"

    def get_absolute_url(self):
        return reverse('b4:plan_detail', args=(self.id,))


class Section(TimeModel):
    name = models.CharField('Название раздела', max_length=255)
    is_active = models.BooleanField('Активный')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['is_active', '-created_at', '-id']

    def __str__(self):
        return self.name


class Task(AbstractSafeModel, TimeModel):
    PRIORITY_CHOICE = (
        (0, "Low"),
        (1, "Medium"),
        (2, "High"),
        (3, "Hot"),
    )

    plan = models.ForeignKey('Plan', verbose_name='План', on_delete=models.CASCADE)
    section = models.ForeignKey('Section', verbose_name='Секция', on_delete=models.SET_NULL, null=True)
    description = models.TextField('Описание')
    is_ready = models.BooleanField('Выполнено', default=False)
    priority = models.IntegerField('Приоритет', choices=PRIORITY_CHOICE, default=PRIORITY_CHOICE[1][0])

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['is_ready', '-priority', '-updated_at', '-created_at', '-id']

    def __str__(self):
        return f"{self.id} {self.plan} {self.section}"

    def get_absolute_url(self):
        return reverse('b4:plan_detail', args=(self.plan_id,))
