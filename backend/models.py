from django.db import models
from django.utils.translation import gettext_lazy as _


class CategoryModel(models.Model):
    title = models.CharField(max_length=40, verbose_name=_('title'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class MealModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.PROTECT,
        related_name='meal',
        verbose_name=_('category')
    )
    ingredients = models.TextField(verbose_name=_('ingredients'))
    image = models.ImageField(upload_to='meal_image', verbose_name=_('image'))
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name=_('price'))
    real_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name=_('real_price'))
    discount = models.DecimalField(
        decimal_places=0,
        max_digits=9,
        default=0,
        verbose_name=_('discount'),
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def is_discount(self):
        return self.discount != 0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('meal')
        verbose_name_plural = _('meal')


class UserModel(models.Model):
    tg_id = models.CharField(max_length=15, verbose_name=_('tg_id'), unique=True)
    contact = models.CharField(max_length=13, verbose_name=_('contact'), default='-')
    lang = models.CharField(max_length=3, verbose_name=_('lang'))
    name = models.CharField(max_length=30, verbose_name=_('name'), default='-')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return f'{self.name} - {self.tg_id}'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class OrderModel(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('user')
    )
    meal = models.ManyToManyField(
        MealModel,
        related_name='order',
        verbose_name=_('meal')
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class CommentModel(models.Model):
    author = models.ForeignKey(
        UserModel,
        on_delete=models.PROTECT,
        related_name=_('comments'),
        verbose_name=_('author')
    )
    comment = models.TextField(verbose_name=_('comment'), default='--')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.author.name

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

