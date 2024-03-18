from fastapi import FastAPI, Header
from pydantic import BaseModel
from src import auth
from src.utils.response import CustomResponse
from src.scrape import common as scrp_cmn
from src.session import common as sessn_cmn
from src.utils import helper as utils
from src import urls
from src.utils.response import CustomResponse, HandleException

import requests
import time
import threading
import random

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
        return HandleException(
            message="Login Unsuccessful", exception=e
        ).send_response()


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

        html_page = session.get(urls.USER_INFO_URL).content.decode("utf-8")
        user_details = scrp_cmn.get_details(html_page)

        html_page = session.get(urls.ATTENDANCE_DUTY_LEAVE_URL).content.decode("utf-8")
        attendance = scrp_cmn.get_total_attendance(html_page)

        user_details.update(attendance)

        return CustomResponse(
            status_code=200, message="Details Fetched", data=user_details
        ).to_dict()

    except Exception as e:
        return HandleException(
            message="Details Fetch Unsuccessful", exception=e
        ).send_response()


@app.get("/get-sidebar/")
def get_sidebar(session_id: str = Header(None, convert_underscores=False)):
    try:
        session = sessn_cmn.get_session(session_id)

        html_page = session.get(urls.USER_INFO_URL).content.decode("utf-8")
        user_details = scrp_cmn.get_sidebar_details(html_page)

        return CustomResponse(
            status_code=200, message="Details Fetched", data=user_details
        )
    except Exception as e:
        return HandleException(
            message="Details Fetch Unsuccessful", exception=e
        ).send_response()


@app.get("/get-assignments/")
def get_assignments(session_id: str = Header(None, convert_underscores=False)):
    try:
        session = sessn_cmn.get_session(session_id)

        html_page = session.get(urls.RESULTS_URL).content.decode("utf-8")
        subjects = scrp_cmn.get_subjects(html_page)

        # TODO: Implement get_assignments: get assignments for each subject
        # assignments = scrp_cmn.get_assignments(html_page, subjects)

        return CustomResponse(
            status_code=200,
            message="Assignments Fetched",
            data=[
                {"name": subject, "assignments": [None, None, None]}
                for subject in subjects
            ],
        ).to_dict()
    except Exception as e:
        return HandleException(
            message="Assignments fetch unsuccessful", exception=e
        ).send_response()


@app.get("/get-attendance/")
def get_attendance(session_id: str = Header(None, convert_underscores=False)):
    try:
        session = sessn_cmn.get_session(session_id)

        html_page = session.get(urls.RESULTS_URL).content.decode("utf-8")
        subjects = scrp_cmn.get_subjects(html_page)

        subjects_info = {subject.split()[0]: {"name": subject} for subject in subjects}

        html_page = session.get(urls.ATTENDANCE_URL).content.decode("utf-8")
        scrp_cmn.get_subject_attendance(html_page, subjects_info)

        html_page = session.get(urls.ATTENDANCE_DUTY_LEAVE_URL).content.decode("utf-8")
        scrp_cmn.get_subject_attendance(html_page, subjects_info)

        utils.get_formatted_attendance(subjects_info)

        return CustomResponse(
            status_code=200,
            message="Attendance Fetched",
            data=list(subjects_info.values()),
        ).to_dict()
    except Exception as e:
        return HandleException(
            message="Attendance Fetch Unsuccessful", exception=e
        ).send_response()


@app.get("/get-timetable/{day}/")
def get_time_table(day: int, session_id: str = Header(None, convert_underscores=False)):
    try:
        session = sessn_cmn.get_session(session_id)

        html_page = session.get(urls.TIMETABLE_URL).content.decode("utf-8")
        time_table = scrp_cmn.get_time_table(html_page, day)

        return CustomResponse(
            status_code=200,
            message="Time Table Fetched",
            data={"day": day, "subjects": list(time_table)},
        ).to_dict()
    except Exception as e:
        return HandleException(
            message="Time Table Fetch Unsuccessful", exception=e
        ).send_response()

    # define a function to send http request to self at 45 - 1 hour intervals
    # randomly to keep the server alive
    # self server url = https://webscrapper-r78p.onrender.com

    # It should run in a separate thread


# Function to send HTTP requests at random intervals to keep the server alive
def keep_server_alive():
    # server_url = "http://127.0.0.1:8000"
    server_url = "https://webscrapper-r78p.onrender.com"
    while True:
        # Generate a random interval between 45 minutes and 1 hour
        interval = random.randint(45 * 60, 60 * 60)
        # interval = random.randint(2, 3)
        try:
            # Send HTTP GET request to the server URL
            index = random.randint(0, 4)
            request_urls = [
                f"{server_url}/get-details/",
                f"{server_url}/get-sidebar/",
                f"{server_url}/get-assignments/",
                f"{server_url}/get-attendance/",
                f"{server_url}/get-timetable/1/",
            ]
            response = requests.get(request_urls[index])
            print(
                f"HTTP GET request sent to {server_url}, Response: {response.status_code}"
            )
        except Exception as e:
            print(f"Failed to send HTTP GET request: {e}")
        # Sleep for the random interval
        time.sleep(interval)


# Run the function in a separate thread
def run_keep_alive_thread():
    keep_alive_thread = threading.Thread(target=keep_server_alive)
    keep_alive_thread.start()


# Start the keep alive thread
run_keep_alive_thread()
