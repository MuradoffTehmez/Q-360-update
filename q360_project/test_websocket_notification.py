import os
import django
import asyncio
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator
from apps.notifications.consumers import NotificationConsumer
from apps.notifications.models import Notification

User = get_user_model()

@sync_to_async
def create_notification(user):
    return Notification.objects.create(
        user=user,
        title='WebSocket Test',
        message='This is a real-time test.',
        notification_type='system'
    )

async def test_websocket():
    print("=== Starting WebSocket Notification Test ===")
    user = await User.objects.aget(username='admin')
    print(f"Testing with user: {user.username}")

    communicator = WebsocketCommunicator(
        NotificationConsumer.as_asgi(), 
        "/ws/notifications/"
    )
    communicator.scope['user'] = user

    connected, subprotocol = await communicator.connect()
    if not connected:
        print("FAIL: WebSocket connection refused.")
        return False
    
    print("WebSocket connected successfully!")
    print("Creating a new notification...")
    
    await create_notification(user)
    
    try:
        response = await communicator.receive_json_from(timeout=5)
        print("Received from WebSocket:", response)
        print("PASS: Notification received in real-time!")
        await communicator.disconnect()
        return True
    except asyncio.TimeoutError:
        print("FAIL: WebSocket did not receive the message within timeout.")
    
    await communicator.disconnect()
    return False

if __name__ == "__main__":
    result = asyncio.run(test_websocket())
    if not result:
        exit(1)
