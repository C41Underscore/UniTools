from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from decouple import config
import argparse


def create_and_parse_args():
    parser = argparse.ArgumentParser(description="A tool to automatically load various minerva pages.")
    parser.add_argument(
        "-p",
        "--page",
        help="The minerva page you would like to load.",
        choices=("Home",
                 "Learn",
                 "Email",
                 "Library",
                 "Services"),
        required=True
    )
    parser.add_argument(
        "-m",
        "--module",
        help="The module/page you would like to access from the Learn page."
    )
    args = parser.parse_args()
    return args


def login(driver):
    username_input = driver.find_element_by_id("userNameInput")
    username_input.send_keys(config("EMAIL"))
    password_input = driver.find_element_by_id("passwordInput")
    password_input.send_keys(config("PASSWORD"))
    login_button = driver.find_element_by_id("submitButton")
    login_button.click()


def switch_to_next_window(driver):
    next_window = driver.window_handles[1]
    driver.close()
    driver.switch_to_window(next_window)


def navigate_learn(driver, module):
    learn_button = driver.find_element_by_id("Learn")
    learn_button.click()
    sleep(1)
    if module is None:
        return
    module_filter = driver.find_element_by_id("ddlTermFilter")
    module_filter.click()
    filter_choices = module_filter.find_elements_by_tag_name("option")
    filter_choices[0].click()
    module_search = driver.find_element_by_id("vleModules_filter").find_element_by_tag_name("input")
    module_search.send_keys(module)
    sleep(1)
    driver.find_element_by_link_text(module.upper()).click()


def navigate_to_email(driver):
    email_button = driver.find_element_by_css_selector(".s1-stud-email.hint--bottom-left")
    email_button.click()
    switch_to_next_window(driver)
    yes_button = driver.find_element_by_id("idSIButton9")
    yes_button.click()
    

def navigate_to_library(driver):
    library_button = driver.find_element_by_css_selector(".s8-stud-lib.hint--bottom")
    library_button.click()
    switch_to_next_window(driver)
    sleep(1)
    login_div = driver.find_element_by_css_selector(".md-button._md-no-style")
    login_div.find_element_by_tag_name("button").click()


def navigate_to_services(driver):
    services_button = driver.find_element_by_css_selector(".s6-stud-ses.hint--bottom")
    services_button.click()
    switch_to_next_window(driver)
    username_input = driver.find_element_by_id("ssSid")
    username_input.send_keys(config("EMAIL"))
    password_input = driver.find_element_by_id("ssPass")
    password_input.send_keys(config("PASSWORD"))
    login_button = driver.find_element_by_css_selector(".loginbutton.ssbtn").find_element_by_tag_name("input")
    login_button.click()


def end_loop(driver):
    while True:
        if driver.window_handles.__len__() == 0:
            try:
                driver.quit()
                exit(0)
            except Exception as e:
                print(e)


def main():
    args = create_and_parse_args()
    opts = Options()
    # opts.add_argument("--kiosk")
    driver = Chrome(options=opts)
    driver.get("https://minerva.leeds.ac.uk")
    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1080)
    login(driver)
    if args.page == "Learn":
        navigate_learn(driver, args.module)
    elif args.page == "Email":
        navigate_to_email(driver)
    elif args.page == "Library":
        navigate_to_library(driver)
    elif args.page == "Services":
        navigate_to_services(driver)
    end_loop(driver)


if __name__ == "__main__":
    main()

# <a class="s8-stud-lib hint--bottom" onclick="_gaq.push(['_trackEvent','Toolbar Widget','library_student_link'])" href="https://leeds.primo.exlibrisgroup.com/discovery/account?vid=44LEE_INST:VU1&amp;section=overview" target="_blank" aria-label="Access your Library account">
# 			<img id="im_hdtoolbar" src="/webapps/UoL-hdtoolbar-bb_bb60/icons/svg/library.svg" onerror="this.src='/webapps/UoL-hdtoolbar-bb_bb60/icons/png/library.png'"></a>