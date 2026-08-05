from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import stripe
from django.urls import reverse
from django.conf import settings
from django.db.models import Sum

from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    items = Item.objects.all()
    orders = Order.objects.all()
    context = {
        'page_title': 'Welcome',
        'items': items,
        'orders': orders,
    }
    return render(request, 'items/home.html', context)

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    context = {
        'page_title': f'Page of {item.name}',
        'item': item,
    }
    return render(request, 'items/item.html', context)

def buy(request, buy_item_id=None, buy_order_id=None):

    if (buy_item_id is None) == (buy_order_id is None):
        return JsonResponse(
            {'error': 'Exactly one purchase object must be specified or object is not specified'},
            status=400,
        )

    def create_line_item(item):
        line_item = {
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(item.price * 100),
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                }
            },
            'quantity': 1,
        }
        return line_item

    line_items = None
    cancel_url = None
    have_discount = False
    discounts = []

    if buy_item_id is not None:
        item = get_object_or_404(Item, pk=buy_item_id)
        line_item = create_line_item(item)
        line_items = [line_item]
        cancel_url = request.build_absolute_uri(
            reverse('item', args=(item.id,))
        )

    elif buy_order_id is not None:
        order = get_object_or_404(Order, pk=buy_order_id)
        line_items = [create_line_item(item) for item in order.items.all()]
        if order.discount is not None:
            discounts = [
                {
                    'coupon': order.discount.stripe_coupon_id
                }
            ]
        if not line_items:
            return JsonResponse(
                {'error': 'The order does not contain any items'},
                status=400,
            )
        cancel_url = request.build_absolute_uri(
            reverse('order', args=(order.id,))
        )



    session = stripe.checkout.Session.create(
        mode = 'payment',
        line_items = line_items,
        success_url = request.build_absolute_uri(
            reverse('success')
        ),
        cancel_url = cancel_url,
        discounts = discounts,
    )
    return JsonResponse({
        'id': session.id,
        'url': session.url
    })

def success(request):
    return render(request, 'items/success.html')

def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    total_price = order.items.aggregate(Sum('price'))['price__sum'] or 0
    context = {
        'page_title': f'Order {order.pk} placement',
        'total_price': total_price,
        'order': order,
    }
    return render(request, 'items/order.html', context)