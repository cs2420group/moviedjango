from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count # Добавили это
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer
from .forms import ItemForm

def home(request):
    query = request.GET.get('search')
    items = Item.objects.all()
    
    if query:
        items = items.filter(title__icontains=query)
    
    total_count = Item.objects.count() # Считаем фильмы

    return render(request, 'reviews/item_list.html', {
        'items': items,
        'search_query': query,
        'total_count': total_count # Передаем в шаблон
    })

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'reviews/item_detail.html', {'item': item})

def about(request):
    return render(request, 'reviews/about.html')

# --- API Эндпоинты ---
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
    

def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'reviews/item_form.html', {'form': form})