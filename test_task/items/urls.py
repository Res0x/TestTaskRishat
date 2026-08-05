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
        views.item_detail,
        name='item',
    ),
    path(
        'item/buy/<int:buy_item_id>',
        views.buy,
        name='item_buy',
    ),
    path(
        'success',
        views.success,
        name='success',
    ),
    path(
        'order/<int:order_id>',
        views.order_detail,
        name='order',
    ),
    path(
        'order/buy/<int:buy_order_id>',
        views.buy,
        name='order_buy',
    ),
]
