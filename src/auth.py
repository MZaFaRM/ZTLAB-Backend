import requests

from .exception import AuthError
from .scrape import common as cmn
from .urls import BASE_URL


def login(username, password):
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
        }
    )
    login_url = f"{BASE_URL}/user/login"
    login_payload = {
        "LoginForm[username]": username,
        "LoginForm[password]": password,
    }
    response = session.post(login_url, data=login_payload)
    cookies = session.cookies.get_dict()
    if not cmn.get_name(response.content.decode("utf-8")):
        raise AuthError("Invalid credentials. Please check your username and password.")

    return cookies
