from django.urls import path, include
from . import views

urlpatterns = [
    path(
        '',
        views.home,
        name='home'
    ),
    path(
        'item/<int:item_id>',
        views.item,
        name='item',
    ),
    path(
        'buy/<int:buy_id>',
        views.buy,
        name='buy',
    ),
    path(
        'success',
        views.success,
        name='success',
    )
]
