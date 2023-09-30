import json
import re
import platform
import time

from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from users_list import UserList


class Followers:

    def initializeDriver(self):
        options = uc.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("enable-automation")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")
        driver = uc.Chrome(options=options, version_main=117, enable_cdp_events=True, headless=True)

        return driver

    def saveToJson(self, resultsList):
        with open('data.json', 'w', encoding='utf-8') as json_file:
            json.dump(resultsList, json_file, ensure_ascii=False, indent=4)

    def convert_to_numeric(self, value_str):
        # Use regular expression to extract numeric values and suffixes (e.g., K, M)
        match = re.match(r'(\d+(\.\d+)?)\s*([KkMm]*)', value_str)
        if match:
            value, _, suffix = match.groups()
            multiplier = {'k': 1000, 'm': 1000000}.get(suffix.lower(), 1)
            return int(float(value) * multiplier)
        else:
            return int(value_str)

    def getUserInfo(self):
        initializeDriver = self.initializeDriver()
        usersList = UserList()
        intagramList = usersList.instagramUsersList()
        resultsList = []

        try:
            for usersInfo in intagramList:
                initializeDriver.get(f"https://www.instagram.com/{usersInfo}")
                print(f"Page loaded for user: {usersInfo}")

                # Wait for the element to be present
                wait = WebDriverWait(initializeDriver, 20)

                getDescriptionElement = "meta[property='og:description']"
                print(f"Waiting for element: {getDescriptionElement}")
                getDescriptionTag = wait.until(
                    ec.presence_of_element_located(
                        (By.CSS_SELECTOR, getDescriptionElement)))
                print(f"{getDescriptionTag}")
                getContent = getDescriptionTag.get_attribute("content")

                stats = getContent.split(", ")
                followers, following, posts = map(
                    self.convert_to_numeric, [stat.split(" ")[0] for stat in stats])

                getTitleElement = "meta[property='og:title']"
                print(f"Waiting for element: {getTitleElement}")
                getTitleTag = wait.until(
                    ec.presence_of_element_located(
                        (By.CSS_SELECTOR, getTitleElement)))
                name = getTitleTag.get_attribute(
                    "content").split("•")[0].strip()

                results = {
                    "name": name,
                    "followers": followers,
                    "following": following,
                    "posts": posts
                }
                resultsList.append(results)

            for finalResult in resultsList:
                print(finalResult)
            self.saveToJson(resultsList)

        except Exception as e:
            raise ValueError(
                f"Couldn't retrieve information for {intagramList}: {e}")

        finally:
            initializeDriver.quit()


if __name__ == "__main__":
    followers = Followers()
    followers.getUserInfo()
    print(platform.platform())
