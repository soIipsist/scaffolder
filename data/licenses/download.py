import os

parent_directory = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
)
os.sys.path.insert(0, parent_directory)

import requests
from bs4 import BeautifulSoup

from utils.file_utils import overwrite_file


def get_license_urls():

    licenses_url = "https://choosealicense.com/appendix/"
    response = requests.get(licenses_url)

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    license_urls = []

    for link in links:
        href = link.get("href")
        href: str
        if href.startswith("/licenses"):
            license_urls.append(f"https://choosealicense.com{href}")

    return license_urls


def download_licenses():
    license_urls = get_license_urls()

    for url in license_urls:
        file_name = os.path.basename(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        pre = soup.find("pre")
        text = pre.get_text()
        print(text)
        print(file_name)
        if not os.path.exists(os.path.join(os.getcwd(), file_name)):
            overwrite_file(file_name, text, "utf-8")


if __name__ == "__main__":
    download_licenses()
