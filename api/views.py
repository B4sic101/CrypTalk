from django.shortcuts import render
from src.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import FRSerializer
from api.models import friendRequest

@api_view(['POST'])
def addContact(request):
    serializer = FRSerializer(data=request.data)
    defaultErrorMsg = "Something went wrong."
    #referer = request.META.get('HTTP_REFERER')
    if serializer.is_valid():
        
        validSer = serializer.validated_data
        if User.objects.filter(userID=validSer['receiver']).exists():
            if User.objects.filter(userID=validSer['sender']).exists():
                if validSer['receiver'] != request.user.userID:

                    if not friendRequest.objects.filter(receiver=validSer['receiver']).exists():
                        newFR = friendRequest.objects.create(receiver=validSer['receiver'], sender=request.user.userID)

                        newFR.save()
                        return Response("Friend request sent!", status=201)
                else:
                    return Response(defaultErrorMsg, status=400)
            else:
                return Response("Friend request already active.", status=300)
        else:
            return Response("This person has already sent you a request.", 200)

    return Response(defaultErrorMsg, status=400)


