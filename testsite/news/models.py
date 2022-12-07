import datetime
from io import BytesIO

from django.core.files import File
from django.db import models
from django.urls import reverse
from PIL import Image


# описываем атрибуты моделей (соотв поля в таблице бд) В моделе будет описываться таблица..
# Создавать поля/колонки в таблицах: id -  INT - создается сам автоматически,если не создаем
#                                    title - Varchar
#                                    content - Text
#                                    created_at - DateTime
#                                    update_at - DateTime
#                                    photo - image
#                                    is_published - Boolean
#  (поля для таблицы новостей) и тп. нельзя использоть заимсв поля/нейминг
# должен быть обязательно подклассом

def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.convert('RGB').save(im_io, 'JPEG', quality=60)
    new_image = File(im_io, name=image.name)
    return new_image


class News(models.Model):
    title = models.CharField(max_length=120, verbose_name='Наименование новости')
    content = models.TextField(blank=False, verbose_name='Контент')
    quotation = models.TextField(blank=False, verbose_name='Короткая цитата новости', null=True)
    created_at = models.DateTimeField(verbose_name='Опубликовано')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(
        upload_to='photo/%Y/%m/%d/', verbose_name='Фото',
        # разбивает фото в папку photo по папкам даты (год, мес, дата)
        blank=False)

    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    recommended = models.BooleanField(default=False, verbose_name='В рекомендуемое?')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True,
                                 verbose_name='Категория')
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'pk': self.pk})

    # нужно продумывать как составлять заранее верно модели, чтобы потом не было проблем.

    def save(self, *args, **kwargs):
        new_image = compress(self.photo)
        self.photo = new_image
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['created_at']


class Category(models.Model):
    # эта модель будет связана с верхней NEWS через ForeignKey
    title = models.CharField(max_length=120, db_index=True, verbose_name='Наименование категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class GroupsTrips(models.Model):
    date_start = models.DateField(blank=True, null=True, verbose_name='Дата начала поездки')
    date_end = models.DateField(blank=True, null=True, verbose_name='Дата окончания поездки')
    trip_text = models.TextField(max_length=1000, blank=True, verbose_name='Дополнительная инфа по поездке')
    trip_price = models.IntegerField(verbose_name='Стоимость поездки')
    trip_place = models.ForeignKey('SkiCenters', on_delete=models.PROTECT, null=True,
                                   verbose_name='Место поездки (выбор ГЛЦ)')
    trip_name_group = models.ForeignKey('Groups', on_delete=models.PROTECT, null=True,
                                        verbose_name='Кто едет')

    class Meta:
        verbose_name = 'ГЛЦ - Расписание поездок'
        verbose_name_plural = 'ГЛЦ - Расписание поездок'


class Groups(models.Model):
    trip_title = models.CharField(max_length=150, verbose_name='Название группы')
    trip_logo = models.ImageField(upload_to='group_logo/', verbose_name='Лого группы', blank=False)
    trip_info = models.TextField(max_length=5000, blank=False, verbose_name='Информация о группе')
    trip_link = models.URLField(max_length=200, verbose_name='Ссылка на группу')

    def __str__(self):
        return self.trip_title

    def save(self, *args, **kwargs):
        new_image = compress(self.trip_logo)
        self.trip_logo = new_image
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'ГЛЦ - Группы'
        verbose_name_plural = 'ГЛЦ - Группы'
        ordering = ['trip_title']


class SkiCenters(models.Model):
    ski_name = models.CharField(max_length=120, db_index=True, verbose_name='Название ГЛЦ')
    ski_info = models.TextField(max_length=5000, blank=False, verbose_name='Информация о ГЛЦ')
    ski_img_one = models.ImageField(upload_to='ski_img/', verbose_name='Фото ГЛЦ 1', blank=False)
    ski_img_two = models.ImageField(upload_to='ski_img/', verbose_name='Фото ГЛЦ 2', blank=False)
    ski_img_three = models.ImageField(upload_to='ski_img/', verbose_name='Фото ГЛЦ 3', blank=False)
    ski_link = models.URLField(max_length=200, verbose_name='Ссылка на ГЛЦ')

    def get_absolute_url(self):
        return reverse('ski_name', kwargs={'ski_name': self.pk})

    def __str__(self):
        return self.ski_name

    class Meta:
        verbose_name = 'ГЛЦ - инфа'
        verbose_name_plural = 'ГЛЦ - инфа'
        ordering = ['ski_name']

# def get_text(url):
#     rs = requests.get(url)
#     root = BeautifulSoup(rs.content, 'html.parser')
#     article = root.select_one('article')
#     return article.text


# class Pubished(models.Model):
#     # эта модель будет связана с верхней NEWS через ForeignKey
#     title = models.CharField(max_length=120, db_index=True, verbose_name='Опубликовано?')
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name = 'Категория'
#         verbose_name_plural = 'Категории'
#         ordering = ['title']
#
