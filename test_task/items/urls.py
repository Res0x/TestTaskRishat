from django.urls import path, include
from . import views

urlpatterns = [
    path(
        '',
        views.home,
        name='home'
    ),
    path(
        'buy/<int:item_id>',
        views.buy,
        name='buy',
    )
]
