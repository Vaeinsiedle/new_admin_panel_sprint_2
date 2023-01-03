import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


GENRE_CHOICES = (
    ('MOVIE', 'movie'),
    ('TV_SHOW', 'tv_show'),
)


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField('name', max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField('description', blank=True)


class Meta:
    # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
    db_table = "genre"
    # Следующие два поля отвечают за название модели в интерфейсе
    verbose_name = 'Жанр'
    verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    certificate = models.CharField(_('certificate'), max_length=512, blank=True)
    # Параметр upload_to указывает, в какой подпапке будут храниться загружемые файлы.
    # Базовая папка указана в файле настроек как MEDIA_ROOT
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    # Типичная модель в Django использует число в качестве id. В таких ситуациях поле не описывается в модели.
    # Вам же придётся явно объявить primary key.
    # Первым аргументом обычно идёт человекочитаемое название поля
    title = models.TextField(_('title'), blank=True)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField('description', blank=True)

    creation_date = models.DateField(blank=True)

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    rating = models.FloatField('rating', blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)] )

    type = models.TextField('type', blank=True, choices=GENRE_CHOICES)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "film_work"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "genre_film_work"


class Gender(models.TextChoices):
    MALE = 'male', _('male')
    FEMALE = 'female', _('female')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField('full_name', max_length=255)
    gender = models.TextField(_('gender'), choices=Gender.choices, null=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "person"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField('role', null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['film_work_id', 'person_id'])
        ]
        db_table = "person_film_work"

