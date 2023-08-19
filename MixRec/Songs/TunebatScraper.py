import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

COOKIE_FOLDER: str = "./Cookie/no_cookies.crx"
TIME_OUT: int = 15


def get_tunebat_data(artist: str, track: str) -> dict:
    tunebat_url = "https://tunebat.com/Search?q=" + artist + "%20" + track

    options = webdriver.ChromeOptions()
    options.add_extension(COOKIE_FOLDER)
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get(tunebat_url)

    try:
        # Connect driver
        WebDriverWait(driver, TIME_OUT).until(EC.title_contains("Tunebat"))
        first_song = driver.find_element(By.CLASS_NAME, "ant-row.pDoqI")
        time.sleep(1.0)  # Wait for the page to fetch the data

        # Click on the first song
        first_song.click()
        time.sleep(1.0)  # redirect

        # get numeric values
        content = driver.find_element(By.CLASS_NAME, "dr-ag").text
        content = content.split("\n")
        values: dict = {}
        for i in range(0, len(content), 2):
            values[content[i + 1]] = content[i]

        # get other values as well such as Key, BPM, etc.
        content = driver.find_element(By.CLASS_NAME, "_5z2l5").text
        content = content.split("\n")
        for i in range(0, len(content), 2):
            values[content[i + 1]] = content[i]

        return values

    except TimeoutException:
        print("Loading took too much time!")
        driver.quit()

    finally:
        driver.quit()

    return {}
