from django.shortcuts import render
from rest_framework import status, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import api_view

# Create your views here.
class getStuffFromCollection(APIView):
    def get(self, request, format=None):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["test"]
        mycol = mydb["messages"]
        x = mycol.find_one()
        return Response({'message':x}, status=status.HTTP_200_OK)
