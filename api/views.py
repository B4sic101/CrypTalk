from src.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import *
from api.models import friendRequest, chat, ChatLine
from django.core import serializers

from secrets import token_bytes
from base64 import b64encode

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
                            if not chat.objects.filter(sender=request.user.userID).exists() and not chat.objects.filter(receiver=request.user.userID).exists():
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
    fr = frRequestChecker(request)
    if fr is not None:

        fr.delete()
        return Response(status=200)
    
    return Response(status=403)

@api_view(['GET'])
def acceptFR(request):
    fr = frRequestChecker(request)
    if fr is not None:
        sender = fr.sender
        fr.delete()

        encryptionKey = b64encode(token_bytes(32)).decode()
        genIV = b64encode(token_bytes(32)).decode()

        newChat = chat.objects.create(sender=sender, receiver=request.user.userID, crypt_key=encryptionKey, iv=genIV)

        username = ""

        if request.user.userID == newChat.receiver:
            username = User.objects.get(userID=newChat.sender).username
        else:
            username = User.objects.get(userID=newChat.receiver).username

        data = {'cryptKey': encryptionKey, 'iv': genIV, 'chatID': newChat.chatID, 'sender': newChat.sender, 'username': username}
        return Response(data, status=201)
    return Response(status=403)

def frRequestChecker(request):
    serializer = FRreceivingSerializer(data=request.query_params)

    if request.user.is_authenticated:
        if serializer.is_valid():

            validSer = serializer.validated_data
            if friendRequest.objects.filter(requestID=validSer['requestID']).exists():

                fr = friendRequest.objects.get(requestID=validSer['requestID'])
                if fr.receiver == request.user.userID:
                    return fr
    return None

@api_view(['GET'])
def getChatDetails(request):
    serializer = getChatDetailsSerializer(data=request.query_params)

    if serializer.is_valid():
        if request.user.is_authenticated:
            if serializer is not None:
                validSer = serializer.validated_data
                chat_obj = chat.objects.get(chatID=validSer["chatID"])
                chatID = validSer["chatID"]
                

                if chat.objects.filter(chatID=chatID, sender=request.user.userID).exists() or chat.objects.filter(chatID=chatID, receiver=request.user.userID).exists():

                    sender = ""
                    username = ""
                    if request.user.userID == chat_obj.receiver:
                        username = User.objects.get(userID=chat_obj.sender).username
                        sender = User.objects.get(userID=chat_obj.sender).userID
                    else:
                        username = User.objects.get(userID=chat_obj.receiver).username
                        sender = User.objects.get(userID=chat_obj.receiver).userID
                    
                    jData = {'cryptKey': chat_obj.crypt_key, 'iv': chat_obj.iv, 'chatID': chat_obj.chatID, 'sender': sender, 'username': username}
                    
                    return Response(jData, status=200)
    
    return Response(status=403)

@api_view(['GET'])
def loadChatMessages(request):
    serializer = getChatDetailsSerializer(data=request.query_params)

    if serializer.is_valid():
        if request.user.is_authenticated:
            if serializer is not None:
                validSer = serializer.validated_data
                chatID = validSer["chatID"]
                

                if chat.objects.filter(chatID=chatID, sender=request.user.userID).exists() or chat.objects.filter(chatID=chatID, receiver=request.user.userID).exists():
                    
                    messagesReturned = ChatLine.objects.filter(chatID=chatID).order_by('time')
                    messages = serializers.serialize('json', messagesReturned)
                    return Response(messages, status=200)
    return Response(status=403)