from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

# allow get requests
@api_view(['GET'])
def getRoutes(request):
    # allows people to connect to allowed endpoints and retreive data from the site
    routes=[
        'GET /api' 
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many = True)
    # python objects are not automatically serializable, turn into json/js object
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many = False)
    # python objects are not automatically serializable, turn into json/js object
    return Response(serializer.data)