from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import datetime
import random
import undetected_chromedriver as uc

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    # Add more user agents if necessary
]

def random_delay(min_seconds=2, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def get_random_user_agent():
    return random.choice(user_agents)

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(f'user-agent={get_random_user_agent()}')
    
    driver = uc.Chrome(options=options)
    return driver

# Function to perform human-like interactions
def perform_human_interaction(driver):
    actions = webdriver.ActionChains(driver)
    actions.move_by_offset(random.randint(0, 100), random.randint(0, 100))
    actions.perform()
    random_delay()
    driver.execute_script("window.scrollBy(0, {});".format(random.randint(200, 800)))
    random_delay()

# Function to login to SINTA using Selenium
def login_sinta(driver, username, password):
    driver.get("https://sinta.kemdikbud.go.id/logins")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    return driver

# Function to login to Elsevier using Selenium
def login_elsevier(driver, username, password):
    driver.get("https://id.elsevier.com/as/authorization.oauth2?platSite=SC%2Fscopus&ui_locales=en-US&scope=openid+profile+email+els_auth_info+els_analytics_info+urn%3Acom%3Aelsevier%3Aidp%3Apolicy%3Aproduct%3Aindv_identity&els_policy=idp_policy_indv_identity_plus&response_type=code&redirect_uri=https%3A%2F%2Fwww.scopus.com%2Fauthredirect.uri%3FtxGid%3De5949ec1f7f8942be40f031fec9c4705&state=userLogin%7CtxId%3DBFEEEC06342ACB062CC06964CAAFD770.i-091fb6f4d2a483d2a%3A5&authType=SINGLE_SIGN_IN&prompt=login&client_id=SCOPUS")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))).click()
    random_delay()
    driver.find_element(By.ID, "bdd-email").send_keys(username)
    random_delay()
    driver.find_element(By.CSS_SELECTOR, "button[value='emailContinue']").click()
    
    # Wait for the password field to be visible and type it
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "bdd-password")))
    random_delay()
    driver.find_element(By.ID, "bdd-password").send_keys(password)
    
    # Wait for the sign-in button to be enabled and clickable
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[value='signin']")))
    random_delay()
    driver.find_element(By.CSS_SELECTOR, "button[value='signin']").click()
    return driver

# Function to get article links from SINTA
def get_article_links(driver, url, num_pages):
    current_year = datetime.datetime.now().year
    target_year = 2021
    done = False

    driver.get(url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "ar-title")))
    
    all_article_links = []
    all_years = []

    for _ in range(num_pages):
        x = 0
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        years = []
        ar_years = soup.find_all('a', class_='ar-year')
        for ar_year in ar_years:
            x += 1
            year = int(ar_year.text.strip())
            if year <= target_year:
                x -= 1
                done = True
                break
            years.append(year)
        
        all_years.extend(years)
        article_links = []
        ar_titles = soup.find_all('div', class_='ar-title')
        for i in range(x):
            link = ar_titles[i].find('a')['href']
            article_links.append(link)
            if len(article_links) == 5:
                article_links.append("https://nowsecure.nl/")
        
        all_article_links.extend(article_links)
        if done:
            break
        if any(year <= target_year for year in years):
            all_years.extend(years)
            break
        try:
            driver.find_element(By.XPATH, "//a[contains(@class,'page-link') and contains(text(),'Next')]").click()
        except:
            break
    return all_article_links, all_years

# Function to scrape articles from Elsevier
def scrape_article(driver, article_links, article_years):
    result = {
        "judul": [],
        "penulis": [],
        "tahun": [],
        "sdgs": [],
        "abstrak": []
    }

    judul = []
    penulis = []
    abstrak = []
    sdgs = []

    for link in article_links:
        driver.get(link)
        random_delay()
        perform_human_interaction(driver)
        penulisBanyak = []
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        judul.append([h2.get_text(strip=True) for h2 in soup.find_all('h2', class_='Typography-module__lVnit Typography-module__o9yMJ Typography-module__JqXS9 Typography-module__ETlt8')])
        abstrak.append([p.get_text(strip=True) for p in soup.find_all('p', class_='Typography-module__lVnit Typography-module__ETlt8 Typography-module__GK8Sg')])
        sdgs.append([div.get_text(strip=True) for div in soup.find_all('div', class_='margin-size-16-b')])
        div_elements = soup.find_all('ul', class_='DocumentHeader-module__LpsWx')
        for div_element in div_elements:
            spans = div_element.find_all('span', class_='Typography-module__lVnit Typography-module__Nfgvc Button-module__Imdmt')
            for span in spans:
                penulisBanyak.append(span.text)
        penulis.append(";".join(penulisBanyak))
    result["judul"] = judul
    result["penulis"] = penulis
    result["tahun"] = article_years
    result["abstrak"] = abstrak
    result["sdgs"] = sdgs
    return result

# Main program
if __name__ == "__main__":
    try:
        username_sinta = "suryoadhiwibowo@telkomuniversity.ac.id"
        password_sinta = "Bangkit2023!"
        username_elsevier = "hamdanazani@student.telkomuniversity.ac.id"
        password_elsevier = "dayak1352"
        num_pages = 1

        # Initialize driver
        driver = create_driver()
        login_sinta(driver, username_sinta, password_sinta)
        target_url_sinta = 'https://sinta.kemdikbud.go.id/affiliations/profile/1093?page=110&view=scopus'
        article_links, article_years = get_article_links(driver, target_url_sinta, num_pages)
        print(article_links)
        print(article_years)

        # Scrape Elsevier
        driver = create_driver()
        login_elsevier(driver, username_elsevier, password_elsevier)
        result = scrape_article(driver, article_links, article_years)

        # Save results to JSON
        df = pd.DataFrame(result)
        df.to_json('testing_sinta_sele.json', orient='records', indent=4)

        # Close the driver
        driver.quit()
    except Exception as e:
        print("Terjadi error:", str(e))
