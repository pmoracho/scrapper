from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_chrome_driver(download_folder, show=False):

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    if not show:
        chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_experimental_option('prefs', {'download.default_directory' : download_folder})

    return webdriver.Chrome(options=chrome_options)