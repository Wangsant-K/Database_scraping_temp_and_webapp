import requests
import selectorlib
import sqlite3
from datetime import datetime
import time

connection = sqlite3.connect("data.db")

URL = "http://programmer100.pythonanywhere.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["temperature"]
    return value


def store(extracted):
    now_time = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO temperatures VALUES(?, ?)", (now_time, extracted))
    connection.commit()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        store(extracted)
        time.sleep(15)
