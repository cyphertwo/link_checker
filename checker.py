import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from utils import clean_text, normalize_url

# ---------------------------
# Vérifie la présence d'un pseudo/mot-clé dans le post
# ---------------------------
def check_post(url, pseudo):
    headers = {
        "User-Agent": "...",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        texts = soup.find_all(string=True)
        for t in texts:
            if clean_text(pseudo) in clean_text(t):
                return True
        return check_post_selenium(url, pseudo)
    except Exception:
        return check_post_selenium(url, pseudo)

# Selenium headless pour check_post
def check_post_selenium(url, pseudo):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    #options.add_argument("user-agent=Mozilla/5.0")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_source = driver.page_source
        driver.quit()
        soup = BeautifulSoup(page_source, 'html.parser')
        texts = soup.find_all(string=True)
        for t in texts:
            if clean_text(pseudo) in clean_text(t):
                return True
        return False
    except Exception:
        try: driver.quit()
        except: pass
        return False

# ---------------------------
# Vérifie la présence d'un lien sur la page
# ---------------------------
def check_link(page_url, link_to_check):
    headers = {
        "User-Agent": "...",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    normalized_check = normalize_url(link_to_check)
    try:
        resp = requests.get(page_url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = soup.find_all("a", href=True)
        for l in links:
            if normalized_check in normalize_url(l.get("href")):
                return True
        return check_link_selenium(page_url, link_to_check)
    except Exception:
        return check_link_selenium(page_url, link_to_check)

# Selenium headless pour check_link
def check_link_selenium(page_url, link_to_check):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    #options.add_argument("user-agent=Mozilla/5.0")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")


    normalized_check = normalize_url(link_to_check)
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(page_url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_source = driver.page_source
        # Dans check_link_selenium()
        #print("=== HTML récupéré par Selenium ===")
        #print(page_source[:1000])
        driver.quit()
        soup = BeautifulSoup(page_source, 'html.parser')
        links = soup.find_all("a", href=True)
        for l in links:
            #print(l)
            if normalized_check in normalize_url(l.get("href")):
                return True
        return False
    except Exception:
        try: driver.quit()
        except: pass
        return False
# ---------------------------

#t=check_link("https://www.genesisforum.it/viewtopic.php?f=32&t=9902", "https://valore2euro.it/")
#print(t)