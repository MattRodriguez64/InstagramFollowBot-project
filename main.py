from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

chrome_driver_path = "./ChromeDriver/chromedriver.exe"
SIMILAR_ACCOUNT = "space_lovers"
INSTAGRAM_ACCOUNT_URL = f"https://www.instagram.com/{SIMILAR_ACCOUNT}/followers/"
USERNAME = "YOUR USERNAME"
PASSWORD = "YOUR PASSWORD"


class InstaFollower:

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)

    def login(self):
        self.driver.get(url="https://www.instagram.com/accounts/login/")
        self.driver.maximize_window()

        try:
            accept_btn = self.driver.find_element_by_xpath(xpath="/html/body/div[4]/div/div/button[1]")
            accept_btn.click()

            sleep(3)

            username_input = self.driver.find_element_by_name(name="username")
            username_input.send_keys(USERNAME)

            password_input = self.driver.find_element_by_name(name="password")
            password_input.send_keys(PASSWORD)

            connect_btn = self.driver.find_element_by_xpath(xpath='//*[@id="loginForm"]/div/div[3]/button/div')
            connect_btn.click()

            sleep(5)

            later_btn = self.driver.find_element_by_xpath(
                xpath='//*[@id="react-root"]/section/main/div/div/div/div/button')
            later_btn.click()

            sleep(10)

            later_notifications = self.driver.find_element_by_xpath(
                xpath="/html/body/div[6]/div/div/div/div[3]/button[2]")
            later_notifications.click()

            sleep(5)

        except NoSuchElementException as error:
            print(f"Error : one/many element(s) is/are missing\n- Message Console -\n{error}")

    def find_followers(self):
        self.driver.get(url=f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")

        sleep(5)

        subscribers_btn = self.driver.find_element_by_partial_link_text(link_text=" abonnés")
        subscribers_btn.click()

        sleep(3)

        popup_followers = self.driver.find_element_by_xpath(xpath="/html/body/div[6]/div/div/div[2]")
        html_scroll = self.driver.find_element_by_tag_name(name="html")

        for i in range(0, 10):
            try:
                popup_followers.click()
                html_scroll.send_keys(Keys.END)
            except StaleElementReferenceException:
                self.driver.back()
                sleep(20)
                popup_followers = self.driver.find_element_by_xpath(xpath="/html/body/div[4]/div/div/div[2]")
                html_scroll = self.driver.find_element_by_tag_name(name="html")

            sleep(3)

        html_scroll.send_keys(Keys.UP)
        sleep(3)

        if self.driver.current_url != INSTAGRAM_ACCOUNT_URL:
            self.driver.back()
            sleep(20)

    def follow(self):
        all_follow_btn = self.driver.find_elements_by_css_selector(css_selector="li button")
        print(len(all_follow_btn))
        if len(all_follow_btn) == 0:
            self.driver.back()
            sleep(20)
            all_follow_btn = self.driver.find_elements_by_css_selector(css_selector="li button")
        else:
            for follow_btn in all_follow_btn:
                try:
                    action = ActionChains(driver=self.driver)
                    action.move_to_element(to_element=follow_btn).perform()
                    follow_btn.click()
                except ElementClickInterceptedException:
                    sleep(1)
                    cancel_btn = self.driver.find_element_by_xpath(xpath="/html/body/div[7]/div/div/div/div[3]/button[2]")
                    cancel_btn.click()
                sleep(1)


bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()
