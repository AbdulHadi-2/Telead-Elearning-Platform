from django.urls import path
from . import views
from .views import UserChatRoomsView, ChatRoomMessagesView

urlpatterns = [
    path('chat-rooms/', UserChatRoomsView.as_view(), name='user-chat-rooms'),
    path('chat-rooms/<int:pk>/', views.ChatRoomDetail.as_view(), name='chat-room-detail'),
    path('chat-rooms/<int:chat_room_id>/messages/', views.MessageList.as_view(), name='message-list'),
    # path('chat-rooms/', views.ChatRoomList.as_view(), name='chat-room-list'),
    # path('chat/<int:chat_room_id>/messages/', ChatRoomMessagesView.as_view(), name='chat-room-messages'),
]

