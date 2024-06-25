import os

parent_directory = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
)

from utils.file_utils import download_file


# TODO: Add all licenses


def download_licenses():
    url = "https://choosealicense.com/licenses"

    licenses = ["unlicense"]

    for l in licenses:
        l_url = f"{url}/{l}"
        print(l_url)
        download_file(l_url)


if __name__ == "__main__":
    download_licenses()
