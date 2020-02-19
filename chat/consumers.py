import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread,ChatMessage

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connected: ",event)
        #accepting websocket connection
        
        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        print(other_user,me)
        thread_obj = await self.get_thread(me,other_user)
        self.thread_obj=thread_obj
        print(me,thread_obj.id)
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            "type":"websocket.accept"
        })
        # await asyncio.sleep(5)
        # await self.send({
        #     "type":"websocket.send",
        #     "text":"You are connected with backend"
        # })
        

    async def websocket_receive(self,event):
        print("received: ",event)
        #receiving the text data from frontend
        front_text = event.get("text",None)
        if front_text is not None:
            load_dic_data = json.loads(front_text)
            msg = load_dic_data.get("message")
            print(msg)
            #getting login user
            me = self.scope['user']
            
            username = 'default'
            if me.is_authenticated:
                username=me.username
                img = me.userprofile.p_photo.url
            myResponse = {
                'message':msg,
                'username': username,
                'image':img
            }
            print(msg," by ",username)
            await self.create_chat_message(me, msg)
            # await self.send({
            #     "type":"websocket.send",
            #     "text": json.dumps(myResponse)
            # })
            #braodcast the msg event to be sent
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"chat_message",
                    "message":json.dumps(myResponse)
                }
            )
    async def chat_message(self,event):
        #this will sends the actual msg
        await self.send({
            "type":"websocket.send",
            "text": event["message"]
        })

    async def websocket_disconnect(self,event):
        print("disconnected: ",event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user,other_username)[0]   

    #storing chat data in database
    @database_sync_to_async
    def create_chat_message(self, me, msg):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj,user=me,message=msg)