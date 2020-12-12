
from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html', {})
# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name': room_name
#     })

def room(request, room_name):
    return render(request, 'chat/roomm.html', {
        'room_name': room_name
    })

def spin(request):
    return render(request, 'chat/roomm.html', {})