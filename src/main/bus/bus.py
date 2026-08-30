import threading

class Bus:
    '''
        Creates a bus with the list of given channels

        Parameters:
            channels: a list of string with the name of the channels.

    '''
    def __init__(self, channels):
        self.listeners = {name: {} for name in channels}
        self._lock = threading.RLock()


    def _get_id(self, cb):
        """
        Returns a stable identifier for a callable.
        """
        if hasattr(cb, "__self__") and hasattr(cb, "__func__"):
            return (id(cb.__self__), cb.__func__)
        return id(cb)


    '''
        Adds listsner to the channel
    '''
    def subscribe(self, channel, listener):
        if channel not in self.listeners:
            raise ValueError(f"Unknown channle: {hannel}")

        cid = self._get_id(listener)
        with self._lock:
            self.listeners[channel][cid] = listener


    def unsubscribe(self, channel, listener):
        if channel not in self.listeners:
            raise ValueError(f"Unknown channle: {hannel}")

        cid = self._get_id(listener)
        with self._lock:
            self.listeners.get(channel, []).pop(cid, None)


    def isSubscribed(self, channel, listener):
        if channel not in self.listeners: return False
        cid = self._get_id(listener)
        return cid in self.listeners[channel]
                

    '''
        Sends a frame to all listeners in the channel.
    '''
    def notify(self, channel, frame):
        with self._lock:
            values = list(self.listeners.get(channel, []).values())

        for listener in values:
            try:
                listener(frame)
            except Exception as ex:
                print(ex)
                self.unsubscribe(channel, listener)
