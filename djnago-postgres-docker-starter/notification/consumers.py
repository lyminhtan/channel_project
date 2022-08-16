import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):

    # join to group
    async def connect(self):
        self.group_name = 'notification'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    # leave group
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # receive message from websocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        event = {
            'type': 'send_message',
            'message': message,
        }
        # send message to group
        await self.channel_layer.group_send(self.group_name, event)

    # receive message from group
    async def send_message(self, event):
        message = event['message']

        # send message to websocket
        await self.send(text_data=json.dumps({'message': message}))

