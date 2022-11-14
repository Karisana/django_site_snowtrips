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
