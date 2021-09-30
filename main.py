from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from os import environ


def getSelectionPage(browser):
    main_form_text = browser.find_element_by_css_selector("#mainForm").get_property("innerText")
    if "Select a date and time" in main_form_text:
        return "DateSelection"
    elif "Group size" in main_form_text:
        return "GroupSizeSelection"
    elif "No more available times" in main_form_text:
        return "NoSelection"
    else:
        return "ErrorSelection"


def selectDate(browser):
    all_dates = browser.find_elements_by_css_selector("div.date.one-queue")
    available_dates = []
    for date in all_dates:
        try:
            date.find_element_by_css_selector("i.fas.fa-exclamation-triangle")
            continue
        except NoSuchElementException:
            available_dates.append(date)

    date_time_map = {}
    for date in available_dates:
        available_times = []
        all_times_css = date.find_elements_by_css_selector("li.time.ampm-format")

        for time in all_times_css:
            if time.get_property("ariaHidden") is None:
                elem = time.find_element_by_css_selector("span.mdc-button__label.available-time")
                available_times.append(elem.get_property("innerHTML"))

        date_time_map[date.text] = available_times

    for k, v in date_time_map.items():
        print(k, ' : ', v)

    print("==================================================")
    print("==================================================")


def makeReservation(activity_name, activity_full_name, browser):
    base_url = "https://reservation.frontdesksuite.ca/rcfs/cardelrec/Home/Index?Culture=en&PageId=a10d1358-60a7-46b6" \
               "-b5e9-5b990594b108&ButtonId=00000000-0000-0000-0000-000000000000 "
    browser.get(base_url)

    for elem in browser.find_elements_by_css_selector('a.button.no-img'):
        if activity_full_name in elem.get_property("innerText"):
            elem.click()
            break

    # 3 possibilities here: no more avail time, select group size, select times
    selection_page = getSelectionPage(browser)

    print("Booking Activity: " + activity_name)
    print("On selection page: " + selection_page)

    if selection_page == "NoSelection":
        print("==================================================")
        print("==================================================")
        return
    elif selection_page == "GroupSizeSelection":
        browser.find_element_by_id("submit-btn").click()
        selectDate(browser)
    elif selection_page == "DateSelection":
        selectDate(browser)


def main():
    opts = Options()
    opts.headless = False
    browser = webdriver.Chrome("C:\\chromedriver", options=opts)
    browser.maximize_window()

    # cardio_full_name = "/rcfs/cardelrec/ReserveTime/StartReservation?pageId=a10d1358-60a7-46b6-b5e9-5b990594b108&buttonId=3dfedc0c-fea9-4c89-bf5b-adc58e05d0d1&culture=en&uiCulture=en "
    # lane_swim_url = "/rcfs/cardelrec/ReserveTime/StartReservation?pageId=a10d1358-60a7-46b6-b5e9-5b990594b108" \
    #                 "&buttonId=c86cf38e-1a0c-4c54-9c35-8761f41a16ad&culture=en&uiCulture=en "
    # public_swim_url = "/rcfs/cardelrec/ReserveTime/StartReservation?pageId=a10d1358-60a7-46b6-b5e9-5b990594b108" \
    #                   "&buttonId=7b98010a-b155-4495-9bad-8c50fe4aeed4&culture=en&uiCulture=en "
    # public_swim_slide_url = "/rcfs/cardelrec/ReserveTime/StartReservation?pageId=a10d1358-60a7-46b6-b5e9-5b990594b108" \
    #                         "&buttonId=e6450c3b-a2a5-4867-aaa9-3840dd51fa6a&culture=en&uiCulture=en "

    cardio_full_name = "Cardio and weight room – 60 minutes"
    lane_swim_url = "Lane swim"
    public_swim_url = "Public swim"
    public_swim_slide_url = "Public swim - With slide"

    all_urls_map = {"cardio_full_name": cardio_full_name, "lane_swim_url": lane_swim_url, "public_swim_url": public_swim_url,
                    "public_swim_slide_url": public_swim_slide_url}

    try:
        for k, v in all_urls_map.items():
            makeReservation(k, v, browser)
    except:
        print("Booking Failed")
    finally:
        browser.quit()


if __name__ == '__main__':
    main()
