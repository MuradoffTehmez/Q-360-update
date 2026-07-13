import logging

logger = logging.getLogger(__name__)

class EventDispatcher:
    """
    A simple in-memory event dispatcher to prepare for Event-Driven Architecture.
    """
    _listeners = {}

    @classmethod
    def subscribe(cls, event_type, listener):
        if event_type not in cls._listeners:
            cls._listeners[event_type] = []
        cls._listeners[event_type].append(listener)

    @classmethod
    def publish(cls, event_type, payload=None):
        logger.info(f"Event published: {event_type}")
        if event_type in cls._listeners:
            for listener in cls._listeners[event_type]:
                try:
                    listener(payload)
                except Exception as e:
                    logger.error(f"Error executing listener for {event_type}: {e}")
