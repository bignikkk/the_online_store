from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=256,
        unique=True,
        verbose_name='Слаг'
    )
    image = models.ImageField(
        upload_to='categories/',
        blank=True, null=True,
        verbose_name='Изображение'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    """Модель субкатегорий."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=256,
        unique=True,
        verbose_name='Слаг'
    )
    image = models.ImageField(
        upload_to='subcategories/',
        blank=True, null=True,
        verbose_name='Изображение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    """Модель продуктов."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=256,
        unique=True,
        verbose_name='Слаг'
    )
    image_small = models.ImageField(
        upload_to='products/small/',
        blank=True, null=True,
        verbose_name='Маленькая картинка'
    )
    image_medium = models.ImageField(
        upload_to='products/medium/',
        blank=True,
        null=True,
        verbose_name='Средняя картинка'
    )
    image_large = models.ImageField(
        upload_to='products/large/',
        blank=True,
        null=True,
        verbose_name='Большая картинка'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Подкатегория'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True,
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Cart(models.Model):
    """Модель корзины."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'

    class Meta:
        ordering = ['id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    """Модель элементы корзины."""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
    )

    def __str__(self):
        return (
            f'{self.quantity} x {self.product.name} '
            f'в корзине пользователя {self.cart.user.username}'
        )

    @property
    def total_price(self):
        return self.quantity * self.product.price

    class Meta:
        ordering = ['id']
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
