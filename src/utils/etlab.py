import contextlib

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://kmctce.etlab.app"
SURVEY_BASE = "survey/user"


class ETLab:
    def __init__(self, session):
        print("\n\nSetting up everything...")
        self.session = session

    def get_surveys(self):
        print(f"Fetching all the forms for you to fill at {BASE_URL}...")
        response = self.session.get(f"{BASE_URL}/{SURVEY_BASE}/viewall")
        html_content = response.content.decode("utf-8")

        soup = BeautifulSoup(html_content, "html.parser")
        if survey_links := soup.find_all("a", string="Do the Survey"):
            print(f"You have {len(survey_links)} form(s) to fill")
            for survey_link in survey_links:
                yield survey_link.get("href")
        else:
            print("No fillable forms found...")

    def complete_surveys(self):
        survey_urls = self.get_surveys()
        for survey_url in survey_urls:
            if data_payload := self.get_answers(survey_url):
                response = self.session.post(
                    f"{BASE_URL}{survey_url}", data=data_payload
                )
                if response.ok:
                    print("Survey submitted successfully....")
                else:
                    print("Survey submission failed...")
            else:
                print("No questions found to answer...")

    def get_answers(self, survey_url):
        print("Generating answers...\n")
        html_content = self.session.get(f"{BASE_URL}{survey_url}").content.decode(
            "utf-8"
        )
        soup = BeautifulSoup(html_content, "html.parser")
        answer_classes = soup.find_all(class_="answer")
        questions = soup.find_all(class_="question")

        data_payload = {}

        for i, answer_class in enumerate(answer_classes):
            # Find the first radio input within the current "answer" class
            first_radio_input = answer_class.find("input", {"type": "radio"})
            print("Question:", questions[i].text.strip())

            # Check if a radio input is found in the current "answer" class
            if first_radio_input:
                # Extract or simulate selection for the first radio input
                print(
                    "Input:", first_radio_input.next_sibling.strip(), "\n"
                )  # Extracting the text content

                data_payload[first_radio_input["name"]] = first_radio_input["value"]
            else:
                print("No radio inputs found in the current 'answer' class.\n")
            print()

        return data_payload


if __name__ == "__main__":
    with contextlib.suppress(Exception):
        print("Hi there!\n")
        print("Enter your creds to start auto filling the form...!")
        ETLab(input("Username: "), input("Password: ")).complete_surveys()
    input("\n\nInput any key to quit...")
