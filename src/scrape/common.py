from bs4 import BeautifulSoup

def get_name(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    icon_user_tag = soup.find("i", class_="icon-user")
    if icon_user_tag and icon_user_tag.parent:
        name_tag = icon_user_tag.parent.find("span", class_="text")
        if name_tag:
            return name_tag.get_text()
    else:
        return False
