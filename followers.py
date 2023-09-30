import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from users_list import UserList
import json


class Followers:

    def initializeDriver(self):
        options = uc.ChromeOptions()
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--headless")
        chromeVersion = "0.6.2"
        chromeDriverPath = f"/path/to/chromedriver_{chromeVersion}"
        service = Service(chromeDriverPath)
        driver = uc.Chrome(service=service, options=options)
        return driver

    def saveToJson(self, resultsList):
        with open('data.json', 'w', encoding='utf-8') as json_file:
            json.dump(resultsList, json_file, ensure_ascii=False, indent=4)

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
                wait = WebDriverWait(initializeDriver, 300)
                """
                og:description
                <meta property="og:description" content="40K Followers, 138 Following, 32 Posts - See Instagram
                photos and videos from xxx (@xxx)">
                """
                getDescriptionElement = "meta[property='og:description']"
                print(f"Waiting for element: {getDescriptionElement}")
                getDescriptionTag = wait.until(
                    ec.presence_of_element_located(
                        (By.CSS_SELECTOR, getDescriptionElement)))
                print (f"{getDescriptionTag}")
                getContent = getDescriptionTag.get_attribute("content")
                """
                getContent.split(", ") = When ", ", then do split
                ---
                followers, following, posts example
                stats = ["40K Followers, 138 Following, 32 Posts", "1.5M Followers, 500 Following, 200 Posts"]
                cleaned_stats = list(map(str.strip, [stat.split(" ")[0] for stat in stats]))
                for result in cleaned_stats:
                    print(result)
                # 40K Followers, 138 Following, 32 Posts
                # 1.5M Followers, 500 Following, 200 Posts
                """
                stats = getContent.split(", ")
                followers, following, posts = map(
                    str.strip, [stat.split(" ")[0] for stat in stats])

                """
                og:title
                <meta property="og:title" content="xxx(@xxx) • Instagram photos and videos">
                """
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
