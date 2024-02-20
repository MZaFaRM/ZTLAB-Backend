import requests
from .scrape import common as cmn


BASE_URL = "https://kmctce.etlab.app"

def login(username, password):
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
        }
    )
    print("\n\nSetting up everything...")

    print(f"Contacting {BASE_URL}...")
    login_url = f"{BASE_URL}/user/login"
    login_payload = {
        "LoginForm[username]": username,
        "LoginForm[password]": password,
    }
    response = session.post(login_url, data=login_payload)
    print("Trying to log in...")
    name = cmn.get_name(response.content.decode("utf-8"))

    if name:
        print(f"Login successful...!")
        print(f"\n\nHello {name.title()}!")
        return session
    else:
        print("Login failed...")
        print("Check your credentials and try again.")
        raise ValueError


