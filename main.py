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
