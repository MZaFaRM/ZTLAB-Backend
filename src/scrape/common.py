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


def get_attendance(html_content):
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

    return {
        "name": name,
        "uni_reg_no": uni_reg_no,
        "admission_no": admission_no,
        "mobile_no": mobile_no,
        "email": email,
        "academic_year": academic_year,
        "address": address,
        "sign": sign,
    }
