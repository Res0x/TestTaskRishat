from django.shortcuts import render, get_object_or_404
from .models import Item


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