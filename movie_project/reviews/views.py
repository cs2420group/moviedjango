from django.shortcuts import render
from .models import Item
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_ some_thing_here_
from .serializers import ItemSerializer


def home(request):
    items = Item.objects.all() 
    return render(request, 'reviews/item_list.html', {'items': items})


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'reviews/item_detail.html', {'item': item})


@api_view(['GET', 'POST'])
def api_test(request):
    if request.method == 'GET':
        
        return Response({"message": "API works!", "status": "success"})
    
    elif request.method == 'POST':
        
        return Response({"message": "Data received!"}, status=status.HTTP_201_CREATED)
    

    @api_view(['GET', 'PUT', 'DELETE'])
def item_api_detail(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)