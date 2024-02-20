from fastapi import FastAPI
from bs4 import BeautifulSoup
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

BASE_URL = "https://kmctce.etlab.app"


def get_name(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    icon_user_tag = soup.find("i", class_="icon-user")
    if icon_user_tag and icon_user_tag.parent:
        name_tag = icon_user_tag.parent.find("span", class_="text")
        if name_tag:
            return name_tag.get_text()
    else:
        return False


def login(username, password, session):
    print(f"Contacting {BASE_URL}...")
    login_url = f"{BASE_URL}/user/login"
    login_payload = {
        "LoginForm[username]": username,
        "LoginForm[password]": password,
    }
    response = session.post(login_url, data=login_payload)
    print("Trying to log in...")
    name = get_name(response.content.decode("utf-8"))

    if name:
        print(f"Login successful...!")
        print(f"\n\nHello {name.title()}!")
        return name.title()
    else:
        print("Login failed...")
        print("Check your credentials and try again.")
        raise ValueError


@app.get("/")
def read_root():
    username = "6424"
    password = "61982e"
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
        }
    )
    print("\n\nSetting up everything...")
    name = login(username, password, session)
    return HTMLResponse(content=f"<h1>Hello {name}!</h1>", status_code=200)
