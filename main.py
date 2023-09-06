import requests
import os
import selectorlib
from datetime import datetime


if not os.path.exists("data.txt"):
    with open("data.txt", "w") as file:
        pass

if not os.path.exists("extract.yaml"):
    with open("extract.yaml", "w") as file:
        pass


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
    with open("data.txt", "a") as file:
        line = f"{now_time}, {extracted}\n"
        print(line)
        file.write(line)


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    store(extracted)
