from fastapi import FastAPI, Header
from pydantic import BaseModel
from src import auth
from utils.response import CustomResponse
from src.scrape import common as scrp_cmn
from src.session import common as sessn_cmn

app = FastAPI()


class Authentication(BaseModel):
    username: str
    password: str


@app.post("/login/")
def login(authentication: Authentication):
    try:
        session = auth.login(authentication.username, authentication.password)
        session_id = sessn_cmn.save_session(session)

        return CustomResponse(
            status_code=200, message="Login Successful", data={"session_id": session_id}
        ).to_dict()

    except Exception as e:
        return CustomResponse(
            status_code=400, message="Login Unsuccessful", error=str(e)
        ).to_dict()


@app.post("/logout/")
def logout(session_id: str = Header(None, convert_underscores=False)):
    try:
        sessn_cmn.delete_session(session_id)
        return CustomResponse(status_code=200, message="Logout Successful").to_dict()

    except Exception as e:
        return CustomResponse(
            status_code=400, message="Logout Unsuccessful", error=str[e]
        ).to_dict()


@app.get("/get-details/")
def get_details(session_id: str = Header(None, convert_underscores=False)):
    try:
        session = sessn_cmn.get_session(session_id)
        html_page = session.get(auth.BASE_URL).content.decode("utf-8")
        
        get_details = scrp_cmn.get_name(html_page)
        return CustomResponse(
            status_code=200, message="Details Fetched", data={"name": get_details}
        ).to_dict()

    except Exception as e:
        return CustomResponse(
            status_code=400, message="Details Fetch Unsuccessful", error=str(e)
        ).to_dict()
