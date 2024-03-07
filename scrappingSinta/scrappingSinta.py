from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Fungsi untuk melakukan login ke SINTA menggunakan Selenium
def login_sinta(username, password):
    # Mengatur opsi browser
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # Membuka browser Chrome
    driver = webdriver.Chrome(options=options)
    
    # Membuka halaman login SINTA
    driver.get("https://sinta.kemdikbud.go.id/logins")

    # Memasukkan username dan password
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)

    # Mengklik tombol login
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    return driver

def login_elsevier(username,password):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # Membuka browser Chrome
    driver = webdriver.Chrome(options=options)

    driver.get("https://id.elsevier.com/as/authorization.oauth2?platSite=SC%2Fscopus&ui_locales=en-US&scope=openid+profile+email+els_auth_info+els_analytics_info+urn%3Acom%3Aelsevier%3Aidp%3Apolicy%3Aproduct%3Aindv_identity&els_policy=idp_policy_indv_identity_plus&response_type=code&redirect_uri=https%3A%2F%2Fwww.scopus.com%2Fauthredirect.uri%3FtxGid%3De5949ec1f7f8942be40f031fec9c4705&state=userLogin%7CtxId%3DBFEEEC06342ACB062CC06964CAAFD770.i-091fb6f4d2a483d2a%3A5&authType=SINGLE_SIGN_IN&prompt=login&client_id=SCOPUS")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "button[id='onetrust-accept-btn-handler']").click()
    time.sleep(1)
    driver.find_element(By.ID, "bdd-email").send_keys(username)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "button[value='emailContinue']").click()
    time.sleep(1)
    driver.find_element(By.ID, "bdd-password").send_keys(password)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "button[value='signin']").click()

    return driver

# Fungsi untuk mendapatkan link artikel dari halaman SINTA
def get_article_links(driver, url, num_pages):
    # Membuka halaman target di SINTA
    driver.get(url)

    # Menggunakan WebDriverWait untuk menunggu hingga elemen pertama muncul
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ar-title")))

    # List untuk menyimpan link artikel dari semua halaman
    all_article_links = []

    # Loop melalui setiap halaman
    for _ in range(num_pages):
        # Menggunakan BeautifulSoup untuk mengekstrak konten
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Mengambil semua link dari setiap judul artikel dalam div dengan class "ar-title"
        article_links = []
        ar_titles = soup.find_all('div', class_='ar-title')
        for ar_title in ar_titles:
            link = ar_title.find('a')['href']
            article_links.append(link)
        
        # Menambahkan link artikel dari halaman ini ke dalam list semua artikel
        all_article_links.extend(article_links)
        
        # Cek apakah ada tombol "Next" untuk navigasi ke halaman berikutnya
        next_button = driver.find_element(By.XPATH, "//a[contains(@class,'page-link') and contains(text(),'Next')]")
        if next_button.get_attribute("href"):
            # Jika ada, klik tombol "Next"
            next_button.click()
            # Tunggu beberapa saat agar halaman selanjutnya dimuat sepenuhnya
            time.sleep(3)
        else:
            # Jika tidak ada tombol "Next", keluar dari loop
            break
    
    return all_article_links
    

def scrape_article(driver, article_links):

    result = {
        "judul": [],
        "penulis": [],
        "sdgs": [],
        "abstrak": []
    }

    judul = []
    penulis = []
    abstrak = []
    sdgs = []

    # Loop melalui setiap link artikel
    for link in article_links:
        # Membuka halaman artikel di Elsevier
        driver.get(link)
        time.sleep()

        # Menggunakan BeautifulSoup untuk mengekstrak konten dari halaman artikel
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        judul.append([h2.get_text(strip=True) for h2 in soup.find_all('h2', class_='Typography-module__lVnit Typography-module__o9yMJ Typography-module__JqXS9 Typography-module__ETlt8')])
        ul_element = soup.find('ul', class_='ul--horizontal margin-size-0')
        penulis.append([li.get_text(strip=True) for li in soup.find('ul', class_='ul--horizontal margin-size-0').find_all('li')])
        abstrak.append([p.get_text(strip=True) for p in soup.find_all('p', class_='Typography-module__lVnit Typography-module__ETlt8 Typography-module__GK8Sg')])
        sdgs.append([div.get_text(strip=True) for div in soup.find_all('div', class_='margin-size-16-b')])

    result["judul"] = judul
    result["penulis"] = penulis
    result["abstrak"] = abstrak
    result["sdgs"] = sdgs

    return result


# Main program
if __name__ == "__main__":
    try:
        # Masukkan username dan password untuk SINTA
        username_sinta = "suryoadhiwibowo@telkomuniversity.ac.id"
        password_sinta = "Bangkit2023!"

        # Masukkan username dan password untuk Elsevier
        username_elsevier = "hamdanazani@student.telkomuniversity.ac.id"
        password_elsevier = "dayak1352"

        # Jumlah halaman yang ingin Anda scrap dari SINTA
        num_pages = 1

        # Login ke SINTA
        driver = login_sinta(username_sinta, password_sinta)

        # Jika login berhasil ke SINTA, dapatkan link artikel dari halaman target di SINTA
        target_url_sinta = 'https://sinta.kemdikbud.go.id/affiliations/profile/1093'
        article_links = get_article_links(driver, target_url_sinta, num_pages)
        print(article_links)

        # Tutup browser SINTA
        driver.quit()

        if article_links:
            # Jika berhasil mendapatkan link artikel, buka browser baru untuk Elsevier
            driver_elsevier = login_elsevier(username_elsevier, password_elsevier)

            # Lakukan scraping pada setiap artikel di Elsevier
            result = scrape_article(driver_elsevier, article_links)

            # Tutup browser Elsevier
            driver_elsevier.quit()

        # Membuat DataFrame dari data
        df = pd.DataFrame(result)

        # Menyimpan DataFrame sebagai file JSON
        df.to_json('result.json', orient='records', indent=4)
    except Exception as e:
        print("Terjadi error:",str(e))