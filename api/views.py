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
        if User.objects.filter(username=validSer['receiver']).exists():
            if validSer['receiver'] != request.user.username:

                if not friendRequest.objects.filter(receiver=validSer['receiver']).exists():
                    newFR = friendRequest.objects.create(receiver=validSer['receiver'], sender=request.user.username)

                    newFR.save()
                    return Response("Friend request sent. Congrats!", status=201)
            else:
                return Response(defaultErrorMsg, status=400)

    return Response(defaultErrorMsg, status=400)


