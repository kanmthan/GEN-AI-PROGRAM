import os
import json
import random
import time
from datetime import datetime

import pandas as pd
from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError
)


# ==============================
# Paths
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONTACT_FILE = os.path.join(
    BASE_DIR,
    "contacts.xlsx"
)

SCREENSHOT_DIR = os.path.join(
    BASE_DIR,
    "screenshots"
)

REPORT_DIR = os.path.join(
    BASE_DIR,
    "reports"
)

SESSION_DIR = os.path.join(
    BASE_DIR,
    "whatsapp_session"
)


os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


DATE = datetime.now().strftime("%Y-%m-%d")

JSON_REPORT = os.path.join(
    REPORT_DIR,
    f"whatsapp_report_{DATE}.json"
)

EXCEL_REPORT = os.path.join(
    REPORT_DIR,
    f"whatsapp_report_{DATE}.xlsx"
)


# ==============================
# Utility functions
# ==============================

def human_delay(page, low=2, high=5):
    """
    Random human-like delay
    """
    seconds = random.randint(low, high)
    page.wait_for_timeout(seconds * 1000)



def load_contacts():

    if not os.path.exists(CONTACT_FILE):
        raise FileNotFoundError(
            "contacts.xlsx not found"
        )


    # Excel engine explicitly defined
    df = pd.read_excel(
        CONTACT_FILE,
        engine="openpyxl"
    )


    required = [
        "Name",
        "Phone",
        "Message"
    ]


    for column in required:
        if column not in df.columns:
            raise Exception(
                f"Missing column: {column}"
            )


    return df.fillna("").to_dict(
        orient="records"
    )



def save_reports(results):

    with open(
        JSON_REPORT,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )


    df = pd.DataFrame(results)

    df.to_excel(
        EXCEL_REPORT,
        index=False
    )


    print("\nReports generated:")
    print(JSON_REPORT)
    print(EXCEL_REPORT)



# ==============================
# WhatsApp functions
# ==============================

def login_whatsapp(page):

    print("Waiting for WhatsApp Web...")

    try:
        page.wait_for_timeout(10000)

        page.wait_for_selector(
            "#pane-side",
            timeout=120000
        )

        print("WhatsApp login successful")
        page.screenshot(path="screenshots/after_login.png")

    except Exception:

        page.screenshot(
            path="screenshots/login_debug.png"
        )

        raise Exception(
            "WhatsApp did not reach chat screen"
        )



def search_contact(page, contact):

    phone = str(contact["Phone"])

    print(f"Searching contact: {phone}")

    try:

        # Wait for WhatsApp chat panel
        page.wait_for_selector(
            "#pane-side",
            timeout=30000
        )


        # Current WhatsApp search input
        search_box = page.locator(
            'input[aria-label="Search or start a new chat"]'
        )


        search_box.wait_for(
            timeout=30000
        )


        search_box.click()


        # Remove + and spaces if present
        phone = (
            phone
            .replace("+", "")
            .replace(" ", "")
        )


        search_box.fill(
            phone
        )


        human_delay(
            page,
            3,
            5
        )


        page.keyboard.press(
            "Enter"
        )


        human_delay(
            page,
            3,
            5
        )


        return True


    except Exception as error:

        print(
            "Search failed:",
            error
        )


        page.screenshot(
            path=os.path.join(
                SCREENSHOT_DIR,
                "search_error.png"
            )
        )


        return False

def send_message(
        page,
        name,
        message
):

    final_message = message.replace(
        "{name}",
        name
    )


    print(
        f"Sending message: {final_message}"
    )


    message_box = page.locator(
        "div[contenteditable='true']"
    ).last


    message_box.wait_for(
        timeout=30000
    )


    message_box.click()


    message_box.fill(
        final_message
    )


    human_delay(
        page
    )


    page.keyboard.press(
        "Enter"
    )


    human_delay(
        page
    )


    return final_message



def capture_screenshot(
        page,
        name
):

    filename = (
        name.replace(" ", "_")
        +
        "_"
        +
        str(int(time.time()))
        +
        ".png"
    )


    path = os.path.join(
        SCREENSHOT_DIR,
        filename
    )


    page.screenshot(
        path=path
    )


    return path



def extract_last_messages(page):

    messages = []

    try:

        message_elements = page.locator(
            "div.copyable-text"
        )


        count = message_elements.count()


        for i in range(
            max(0, count - 3),
            count
        ):

            text = (
                message_elements
                .nth(i)
                .inner_text()
            )


            if text.strip():

                messages.append(
                    text
                )


    except Exception:

        pass


    return messages[-3:]



# ==============================
# Main
# ==============================

def main():

    contacts = load_contacts()

    results = []


    with sync_playwright() as p:


        browser = p.chromium.launch_persistent_context(
            SESSION_DIR,
            headless=False
        )


        page = browser.new_page()


        page.goto(
            "https://web.whatsapp.com"
        )


        login_whatsapp(
            page
        )


        for contact in contacts:


            name = str(
                contact["Name"]
            )

            phone = str(
                contact["Phone"]
            )

            message = str(
                contact["Message"]
            )


            result = {

                "name": name,

                "phone": phone,

                "status": "FAILED",

                "sent_message": "",

                "screenshot": "",

                "last_messages": []

            }


            try:

                found = search_contact(
                    page,
                    contact
                )


                if not found:

                    result["status"] = (
                        "CONTACT_NOT_FOUND"
                    )

                    results.append(
                        result
                    )

                    continue


                sent = send_message(
                    page,
                    name,
                    message
                )


                result["sent_message"] = sent


                result["screenshot"] = (
                    capture_screenshot(
                        page,
                        name
                    )
                )


                result["last_messages"] = (
                    extract_last_messages(
                        page
                    )
                )


                result["status"] = "SENT"



            except Exception as error:


                result["status"] = "FAILED"

                result["error"] = str(error)



            results.append(
                result
            )


            human_delay(
                page,
                3,
                5
            )


        save_reports(
            results
        )


        browser.close()



if __name__ == "__main__":

    main()