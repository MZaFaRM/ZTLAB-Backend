from uuid import uuid4
from collections import OrderedDict
from ..exception import AuthError

MAX_SESSIONS = 10
SESSIONS = OrderedDict()


def save_session(session):
    global SESSIONS
    session_id = str(uuid4())
    SESSIONS[session_id] = session
    
    if len(SESSIONS) > MAX_SESSIONS:
        SESSIONS.popitem(last=False)
    
    print(len(SESSIONS))
    return session_id


def delete_session(session_id):
    global SESSIONS
    SESSIONS.pop(session_id) if session_id in SESSIONS else None
    return True


def get_session(session_id):
    global SESSIONS
    if session_id not in SESSIONS:
        raise AuthError("Invalid auth token. Please login again.")
    return SESSIONS[session_id]
