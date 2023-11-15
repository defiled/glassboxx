import threading
import uuid

class RequestIDManager:
    """
    Manages request IDs within a thread. This ensures that each web request
    (handled in a separate thread in most web frameworks) has a unique request ID.
    """
    _thread_local = threading.local()

    @staticmethod
    def get_request_id():
        """
        Retrieves the current request ID for the thread. If the thread does not have
        a request ID yet, it generates a new one.

        :return: The unique request ID for the current thread.
        """
        if not hasattr(RequestIDManager._thread_local, 'request_id'):
            RequestIDManager._thread_local.request_id = str(uuid.uuid4())
        return RequestIDManager._thread_local.request_id
