from django.db import models


# Create your models here.
class Category(models.Model):
    name_ru = models.CharField(max_length=80, verbose_name='Название категории (русский)')
    name_uz = models.CharField(max_length=80, verbose_name='Название категории (узбекс)')

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name_ru


class Product(models.Model):
    name_ru = models.CharField(max_length=80, verbose_name='Название блюда (русский)')
    name_uz = models.CharField(max_length=80, verbose_name='Название блюда (узбекс)')
    desc_ru = models.TextField(blank=True, verbose_name='Описание блюда (русский)')
    desc_uz = models.TextField(blank=True, verbose_name='Описание блюда (узбекс)')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товара')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    photo = models.ImageField(upload_to='media', verbose_name='Фотография блюда')

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name_ru
