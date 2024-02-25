import re
from bs4 import BeautifulSoup
from .constants import DEPARTMENTS
from .. import urls
from . import helper


def get_name(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    icon_user_tag = soup.find("i", class_="icon-user")
    if icon_user_tag and icon_user_tag.parent:
        if name_tag := icon_user_tag.parent.find("span", class_="text"):
            return name_tag.get_text()
    else:
        return False


def get_details(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    name_row = soup.find("th", text="Name").find_next_sibling("td")

    img_tag = soup.find("img", id="photo")
    img = img_tag["src"]

    name = name_row.text.strip()

    # Find the span tag containing the "Studying in" text
    span_tag = soup.find("center")
    text = span_tag.get_text(strip=True)

    text = text.replace("Studying in", "").strip()

    _, department, year = text.split()
    department = DEPARTMENTS[department] if department in DEPARTMENTS else department

    return {
        "name": name,
        "profile_pic": urls.BASE_URL + img,
        "department": department,
        "year": int(year),
    }


def get_total_attendance(html_content):
    soup = BeautifulSoup(html_content, "html.parser").find("tbody").find("tr")

    tds = soup.find_all("td")

    # Find the <td> element containing the roll number
    roll_number = tds[1].text.strip()

    # Find the <td> element containing the percentage
    percentage = tds[-2].text.strip()[:-1]

    return {
        "roll_number": int(roll_number),
        "attendance": int(percentage),
    }


def get_sidebar_details(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    get_value = lambda x: soup.find("th", text=x).find_next_sibling("td").text.strip()

    name = get_value("Name")
    uni_reg_no = get_value("University Reg No")
    admission_no = get_value("Admission No")
    mobile_no = get_value("Mobile No")

    email = soup.find("th", text="Email").find_next_sibling("td").a["data-cfemail"]
    email = helper.decodeEmail(email)

    academic_year = get_value("Academic Year")
    address = (
        soup.find("span", text="Permanent Address")
        .parent.find("th", text="State")
        .find_next_sibling("td")
        .text.strip()
    )
    sign = urls.BASE_URL + soup.find("img", id="sign")["src"]

    img_tag = soup.find("img", id="photo")
    img = img_tag["src"]

    return {
        "name": name,
        "uni_reg_no": uni_reg_no,
        "admission_no": admission_no,
        "mobile_no": mobile_no,
        "email": email,
        "academic_year": academic_year,
        "address": address,
        "sign": sign,
        "profile_pic": urls.BASE_URL + img,
    }


def get_subjects(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    rows = (
        soup.find(
            "table", class_="items table table-striped table-bordered table-condensed"
        )
        .find("tbody")
        .find_all("tr")
    )

    return [row.find_all("td")[1].get_text().strip() for row in rows[:-1]]


def get_assignments(html_content, subjects):
    pass


def get_subject_attendance(html_content, subjects):

    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    head = table.find("thead").find("tr")
    body = table.find("tbody").find("tr")

    pattern = r"\d+/\d+"
    html_subjects = head.find_all("th", class_="span2")
    html_attendance = body.find_all("td", class_="span2")

    for subject in html_subjects:
        if (subject_name := subject.get_text().strip()) in subjects:
            subject_index = html_subjects.index(subject)
            attendance = html_attendance[subject_index].get_text().strip()

            match = re.match(pattern, attendance)

            present_classes, total_classes = map(int, match.group().split("/"))

            if "present_classes" in subjects[subject_name]:
                subjects[subject_name]["duty_leaves"] = abs(
                    present_classes - subjects[subject_name]["present_classes"]
                )

            subjects[subject_name].update(
                {
                    "present_classes": int(present_classes),
                    "total_classes": int(total_classes),
                }
            )

    return subjects
