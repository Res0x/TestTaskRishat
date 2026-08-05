from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=100)
    percent = models.DecimalField(max_digits=5, decimal_places=2)
    stripe_coupon_id = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(
        Item,
        related_name='orders',
        blank=True,
    )
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order {self.pk}'