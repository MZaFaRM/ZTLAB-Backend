from bs4 import BeautifulSoup
from .constants import BRANCHES, DEPARTMENTS
from .. import urls


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

    branch, department, year = text.split()
    branch = BRANCHES[branch]
    department = DEPARTMENTS[department]

    return {
        "name": name,
        "profile_pic": urls.BASE_URL + img,
        "branch": branch,
        "department": department,
        "year": year,
    }


def get_attendance(html_content):
    soup = BeautifulSoup(html_content, "html.parser").find("tbody").find("tr")

    tds = soup.find_all("td")

    # Find the <td> element containing the roll number
    roll_number = tds[1].text.strip()

    # Find the <td> element containing the percentage
    percentage = tds[-2].text.strip()

    return {
        "roll_number": roll_number,
        "percentage": percentage,
    }
