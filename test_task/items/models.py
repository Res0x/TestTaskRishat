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