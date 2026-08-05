from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import stripe
from django.urls import reverse
from django.conf import settings

from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    items = Item.objects.all()
    context = {
        'page_title': 'Welcome',
        'items': items,
    }
    return render(request, 'items/home.html', context)

def item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    context = {
        'page_title': f'Page of {item.name}',
        'item': item,
    }
    return render(request, 'items/item.html', context)

def buy(request, buy_id):
    item = get_object_or_404(Item, pk=buy_id)
    name = item.name
    description = item.description
    price = int(item.price * 100)
    session = stripe.checkout.Session.create(
        mode = 'payment',
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': price,
                    'product_data': {
                        'name': name,
                        'description': description,
                    }
                },
                'quantity': 1,
            }
        ],
        success_url = request.build_absolute_uri(
            reverse('success')
        ),
        cancel_url = request.build_absolute_uri(
            reverse('item', args=(item.id,))
        )
    )
    return JsonResponse({
        'id': session.id,
        'url': session.url
    })

def success(request):
    return render(request, 'items/success.html')