from django.shortcuts import render,redirect, reverse
from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId
from .forms import PinForm, CreateRoomForm, CreateMessageForm
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from bson.json_util import dumps
from rest_framework import status, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import api_view
from pprint import pprint
import datetime

client = MongoClient('localhost', 27017)
db = client.test
chat_room_collection = db.chatRoom
messagesCollection = db.messages


#JsonResponse(dumps(list(messages.find({'name':'Shannon Brown'}))),safe=
#    ...: False)

# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PinForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            chat = chat_room_collection.find_one({'pin': form.cleaned_data['pin']})
            #print('pin : ' + str(form.cleaned_data['pin']))
            chatID = chat['_id']
            #print(chat_room_collection.find_one({'pin': str(form.cleaned_data['pin'])})['_id'])
            #chatID = chat['_id']
            # redirect to a new URL:
            return redirect(reverse('chat:room', kwargs={'id':chatID}))
            #return render(request, 'chat/room.html', {'pin': form.cleaned_data['pin']})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PinForm()

    return render(request, 'chat/index.html', {'form': form})



def createChat(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateRoomForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            name = form.cleaned_data['name']
            pin = form.cleaned_data['pin']
            chat_room_collection.insert({'name': name, 'pin': pin})
            # redirect to a new URL:
            return redirect(reverse('chat:room', kwargs={'pin':pin}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateRoomForm()

    return render(request, 'chat/create.html', {'form':form})

def enterChat(request):
    pin = chat_room_collection.find({'pin': '1234'})
    context = {'collection': pin}
    return render(request, 'chat/enter.html', context)

def room(request, id):
    #print(pin)
    chatName = chat_room_collection.find_one({'_id': ObjectId(id)})['name']
    messages = messagesCollection.find({'room': ObjectId(id)}).sort("timestamp", DESCENDING)
    context = {
        'name':chatName,
        'messages':messages,
        'id': id,
    }


    return render(request, 'chat/room.html', context)

class getStuffFromCollection(APIView):
    def get(self, request, format=None):
        messages = messagesCollection.find({'room': ObjectId(request.GET.get("room"))}).sort("timestamp", 1)
        newMessages = []
        for message in messages:
            message.pop('_id')
            message.pop('room')
            newMessages.append(message)
        return Response({'thingINeed':newMessages}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        x = messagesCollection.insert_one({"name": request.POST.get("name"), "message": request.POST.get("message"), "timestamp": datetime.datetime.now(), "room": ObjectId(request.POST.get("room"))})
        return Response({'status':"success","message": request.POST.get("message")}, status=status.HTTP_200_OK)

'''@api_view(['GET', 'POST'])
def hello_world(request):
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["test"]
    mycol = mydb["messages"]
    x = mycol.find_one()
    x["id"] = str(x["id"])

    return Response({'message':x}, status=status.HTTP_200_OK)'''


'''@csrf_exempt
def message_list(request):
    """
    List all messages, or create a new message.
    """
    if request.method == 'GET':
        return JsonResponse(dumps(list(messagesCollection.find({'name':'Shannon Brown'}))), safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(dumps(list(messagesCollection.find({'name':'Shannon Brown'}))),status=201)
        return JsonResponse("Error", status=400)'''
