from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer

# --- HTML страницы для браузера ---


def home(request):
    query = request.GET.get('search')
    if query:
        # Ищем фильмы, где в названии есть то, что ввел пользователь
        items = Item.objects.filter(title__icontains=query)
    else:
        items = Item.objects.all()
    
    return render(request, 'reviews/item_list.html', {
        'items': items,
        'search_query': query # Передаем запрос обратно в шаблон
    })

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'reviews/item_detail.html', {'item': item})

def about(request):
    return render(request, 'reviews/about.html')

# --- API Эндпоинты (Пункт 3 задания) ---

@api_view(['GET', 'POST'])
def item_api_list(request):
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def item_api_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)