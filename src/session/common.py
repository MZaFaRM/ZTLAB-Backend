from uuid import uuid4

SESSIONS = {}


def save_session(session):
    global SESSIONS
    session_id = str(uuid4())
    SESSIONS[session_id] = session
    return session_id


def delete_session(session_id):
    global SESSIONS
    SESSIONS.pop(session_id) if session_id in SESSIONS else None
    return True


def get_session(session_id):
    global SESSIONS
    if session_id not in SESSIONS:
        raise ValueError("Invalid auth token. Please login again.")
    return SESSIONS[session_id]
