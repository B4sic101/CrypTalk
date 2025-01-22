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
    if request.data != {}:

        if serializer.is_valid():
            
            validSer = serializer.validated_data
            if validSer['receiver'] != request.user.userID:

                if not friendRequest.objects.filter(receiver=validSer['receiver'], sender=request.user.userID).exists():
                    if not friendRequest.objects.filter(receiver=request.user.userID, sender=validSer['receiver']).exists():
                        newFR = friendRequest.objects.create(receiver=validSer['receiver'], sender=request.user.userID)

                        createdfr = newFR.save()
                        updateFriendRequest(request, createdfr)

                        return Response({"Friend request sent."}, status=201)
                    else:
                        return Response("This user has already sent a request to you.", status=400)
                else:
                    return Response("Already pending request.", status=400)
            else:
                return Response("Cant send a request to yourself.", status=400)
        else:
            return Response("Invalid request.", status=400)
    else:
        return Response("User doesn't exist.", status=404)

    return Response(defaultErrorMsg, status=400)

@api_view(['GET'])
def getUserID(request):
    serializer = getUserIDSerializer(data=request.query_params)
    if serializer.is_valid():
        validSer = serializer.validated_data
        user = User.objects.filter(username=validSer['username'])
        if user.exists():
            data = user.values('userID')[0]
            
            return Response(data, status=200)
        else:
            return Response('User doesnt exist')
    return Response("Invalid data")

def updateFriendRequest(request, createdfr):
    receiver = User.objects.filter(username=createdfr.receiver)
    requestGroups = receiver.requestGroups.filter()