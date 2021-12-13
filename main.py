from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import os
import urllib.request
import sys
import string
import random

service = Service(GeckoDriverManager().install())
service.start()
mainUrl = 'https://unsplash.com/s/photos/'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# --------------------------------------------------- Get User Agent -------------------------------------------------- #
def get_user_agent():
    software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
    operating_systems = [OperatingSystem.WINDOWS.value,
                         OperatingSystem.LINUX.value]
    return UserAgent(software_names=software_names, operating_systems=operating_systems, limit=200).get_random_user_agent()


# ----------------------------------------------- Get firefox driver -------------------------------------------------- #
def get_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument("user-agent=" + str(get_user_agent()))
    driver = webdriver.Firefox(service=service, options=options)
    return driver


# -------------------------------------------------- Loop Images ----------------------------------------------------- #
def loop_images(images, path):
    for image in images:
        url = image.find('img')['src']
        get_image(url=url, path=path)


# --------------------------------------------------- Get Image ------------------------------------------------------ #
def get_image(url, path):
    try:
        img_name = path + '/' + \
            ''.join(random.choices(string.ascii_uppercase +
                    string.digits, k=10)) + '.png'
        print(img_name)
        (filename, headers) = urllib.request.urlretrieve(
            url=url, filename=img_name)
    except Exception as e:
        print('\033[91m' + 'import => ' + str(e) + '\033[91m')
    return 0


# ---------------------------------------------- Check to load more -------------------------------------------------- #
def check_pagination(soup):
    pagination = soup.find_all("a", string="Load more photos")
    if(pagination):
        return True
    return False


# --------------------------------------------------- Get Image ------------------------------------------------------ #
def init(categorie, DirName):
    driver = get_driver()
    driver.get(mainUrl + categorie)
    driver.implicitly_wait(7)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    cpt = 0
    images = soup.find_all('figure')
    loop_images(images=images[cpt:len(images)], path=DirName)
    pagination = check_pagination(soup)
    while(pagination):
        cpt += 20
        if(pagination):
            loop_images(images=images[cpt:len(images)], path=DirName)
            pagination = check_pagination(soup)


# ----------------------------------------------- Lunch Script (Main) ------------------------------------------------ #
if __name__ == '__main__':
    try:
        if(len(sys.argv) > 1):
            categorie = str(sys.argv[1])
            print(bcolors.OKBLUE + "Categorie : " + categorie + bcolors.OKBLUE)
            if(not os.path.isdir(os.getcwd() + '/data')):
                os.mkdir(os.getcwd() + '/data')
            dataPath = os.getcwd() + '/data/' + categorie
            if(not os.path.isdir(dataPath)):
                os.mkdir(os.getcwd() + '/data/' + categorie)
            init(categorie=categorie,  DirName=dataPath)
    except Exception as e:
        print(bcolors.FAIL + 'main => ' + str(e) + bcolors.FAIL)
