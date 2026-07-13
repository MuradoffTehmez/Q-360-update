import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = f"notifications_{self.user.id}"

            # Join user notification group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        # Leave user notification group
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        action = text_data_json.get('action', '')

        # Handle different actions
        if action == 'read_notification':
            notification_id = text_data_json.get('notification_id')
            if notification_id:
                success = await self.mark_notification_as_read(notification_id)
                await self.send(text_data=json.dumps({
                    'type': 'notification_read',
                    'notification_id': notification_id,
                    'success': success,
                    'timestamp': timezone.now().isoformat()
                }))
        elif action == 'read_all':
            count = await self.mark_all_notifications_as_read()
            await self.send(text_data=json.dumps({
                'type': 'all_notifications_read',
                'count': count,
                'timestamp': timezone.now().isoformat()
            }))

    # Receive message from room group
    async def notification_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message,
            'timestamp': timezone.now().isoformat()
        }))

    @database_sync_to_async
    def mark_notification_as_read(self, notification_id):
        """Mark a single notification as read in the database."""
        from apps.notifications.models import Notification
        try:
            updated = Notification.objects.filter(
                pk=notification_id,
                user=self.user,
                is_read=False
            ).update(is_read=True, read_at=timezone.now())
            return updated > 0
        except (ValueError, Notification.DoesNotExist):
            return False

    @database_sync_to_async
    def mark_all_notifications_as_read(self):
        """Mark all unread notifications as read for the current user."""
        from apps.notifications.models import Notification
        count = Notification.objects.filter(
            user=self.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        return count