# Generated by Django 4.1.2 on 2022-12-06 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_alter_news_recommended'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_pk', models.CharField(db_index=True, max_length=120, verbose_name='Категория поездки')),
            ],
            options={
                'verbose_name': 'Наименование места поездки',
                'ordering': ['trip_pk'],
            },
        ),
        migrations.CreateModel(
            name='GroupsTrips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_trip', models.CharField(max_length=150, verbose_name='Название группы')),
                ('logo_trip', models.ImageField(upload_to='group_logo/', verbose_name='Лого группы')),
                ('info_trip', models.TextField(max_length=5000, verbose_name='Информация о группе')),
                ('link_trip', models.URLField(verbose_name='Ссылка на группу')),
                ('date_trip', models.DateTimeField(verbose_name='Дата поездки')),
                ('price_trip', models.IntegerField(verbose_name='Стоимость поездки')),
                ('group_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='news.groupcategory', verbose_name='Категория поездки')),
            ],
            options={
                'verbose_name': 'Выезды с группой',
                'verbose_name_plural': 'Выезды с группой',
                'ordering': ['title_trip'],
            },
        ),
    ]