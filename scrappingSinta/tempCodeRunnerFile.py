def get_article_links(driver, url, num_pages):
    # Membuka halaman target di SINTA
    driver.get(url)

    # Menggunakan WebDriverWait untuk menunggu hingga elemen pertama muncul
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ar-title")))

    # List untuk menyimpan link artikel dari semua halaman
    all_article_links = []

    all_years = []

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

        # Mengambil semua tahun dari setiap link
        years = []
        ar_years = soup.find_all('a', class_='ar-year')
        for ar_year in ar_years:
            year = ar_year.text.strip()
            years.append(year)
        
        # Menambahkan tahun-tahun ini ke dalam list semua tahun
        all_years.extend(years)

        
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
    
    return all_article_links, all_years