from django.shortcuts import render
from src.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import FRSerializer, getUserIDSerializer
from api.models import friendRequest

@api_view(['POST'])
def addContact(request):
    serializer = FRSerializer(data=request.data)
    defaultErrorMsg = "Something went wrong."
    #referer = request.META.get('HTTP_REFERER')
    if serializer.is_valid():
        
        validSer = serializer.validated_data
        if User.objects.filter(userID=validSer['receiver']).exists():
            if validSer['receiver'] != request.user.userID:

                if not friendRequest.objects.filter(receiver=validSer['receiver'], sender=request.user.userID).exists():
                    if not friendRequest.objects.filter(receiver=request.user.userID, sender=validSer['receiver']).exists():
                        newFR = friendRequest.objects.create(receiver=validSer['receiver'], sender=request.user.userID)

                        newFR.save()
                        return Response("Friend request sent!", status=201)
                    else:
                        return Response("This user has already sent a request to you.")
                else:
                    return Response("Already pending request.")
            else:
                return Response("Cant send a request to yourself", status=400)
        else:
            return Response("User doesnt exist", status=404)
    else:
        return Response("Invalid request", status=400)

    return Response(defaultErrorMsg, status=400)

@api_view(['GET'])
def getUserID(request):
    serializer = getUserIDSerializer(data=request.query_params)
    if serializer.is_valid():
        validSer = serializer.validated_data
        
        user = User.objects.filter(username=validSer['username']).values('userID')
        data = user[0]
        
        return Response(data, status=200)
    return Response("Invalid data")