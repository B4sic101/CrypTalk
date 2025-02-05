from django.shortcuts import render
from src.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import FRSerializer, getUserIDSerializer, FRreceivingSerializer
from api.models import friendRequest, chat

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@api_view(['POST'])
def addContact(request):
    serializer = FRSerializer(data=request.data)
    defaultErrorMsg = {'msg':'Something went wrong.', 'requestID':f'{None}'}

    if request.user.is_authenticated:
        if request.data != {}:

            if serializer.is_valid():
                
                validSer = serializer.validated_data

                if validSer['receiver'] != request.user.userID:

                    if not friendRequest.objects.filter(receiver=validSer['receiver'], sender=request.user.userID).exists():
                        if not friendRequest.objects.filter(receiver=request.user.userID, sender=validSer['receiver']).exists():
                            if not chat.objects.filter(receiver=request.user.userID).exists():
                                newFR = friendRequest.objects.create(receiver=validSer['receiver'], sender=request.user.userID)

                                newFR.save()

                                return Response({'msg':'Friend request sent.', 'requestID':f'{newFR.requestID}'}, status=201)
                            else:
                                return Response({'msg':'You already added this contact.', 'requestID':f'{None}'}, status=400)
                        else:
                            return Response({'msg':'This user has already sent a request to you.', 'requestID':f'{None}'}, status=400)
                    else:
                        return Response({'msg':'Already pending request.', 'requestID':f'{None}'}, status=400)
                else:
                    return Response({'msg':'Cant send a request to yourself', 'requestID':f'{None}'}, status=400)
            else:
                return Response({'msg':"Invalid request.", 'requestID':f'{None}'}, status=400)
        else:
            return Response({'msg':'User does not exist.', 'requestID':f'{None}'}, status=404)

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
            return Response('')
    return Response("Invalid data")

@api_view(['GET'])
def rejectFR(request):
    serializer = FRreceivingSerializer(data=request.query_params)
    
    if request.user.is_authenticated:
        if serializer.is_valid():

            validSer = serializer.validated_data
            if friendRequest.objects.filter(requestID=validSer['requestID']).exists():

                fr = friendRequest.objects.get(requestID=validSer['requestID'])
                if fr.receiver == request.user.userID:

                    fr.delete()
                    return Response(status=200)
    
    return Response(status=403)

@api_view(['GET'])
def acceptFR(request):
    serializer = FRreceivingSerializer(data=request.query_params)
    if request.user.is_authenticated:
        if serializer.is_valid():

            validSer = serializer.validated_data
            if friendRequest.objects.filter(requestID=validSer['requestID']).exists():
                fr = friendRequest.objects.get(requestID=validSer['requestID'])

                if fr.receiver == request.user.userID:
                    sender = fr.sender
                    fr.delete()

                    newChat = chat.objects.create(sender=sender, receiver=request.user.userID)
                    data = {'key': f'{newChat}'}

                    return Response(data, status=201)
    return Response(status=403)