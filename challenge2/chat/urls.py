from django.urls import path, include
from . import views


app_name = 'chat'
urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.createChat, name="create"),
    path('enter/', views.enterChat, name="enter"),
    path('room/<id>', views.room, name="room"),
    path('getStuffFromCollection/', views.getStuffFromCollection.as_view(), name="stuff"),
    path('getStuffFromCollection/<message>', views.getStuffFromCollection.as_view(), name="addStuff"),
]
