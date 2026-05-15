import time
import random
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def print_log(text):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {text}", flush=True)

def run_bot():
    # Daftar link video manual kamu
    video_links = [
        "https://www.febspot.com/video/3218504", "https://www.febspot.com/video/3218505",
        "https://www.febspot.com/video/3218527", "https://www.febspot.com/video/3218528",
        # ... (Masukkan sisa link kamu di sini)
        "https://www.febspot.com/video/3141587", "https://www.febspot.com/video/3141592"
    ]

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--mute-audio")
    
    # WAJIB UNTUK TOR
    chrome_options.add_argument('--proxy-server=http://127.0.0.1:8118')
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    print_log(">>> Menyiapkan Browser (Tor Mode)...")
    # Langsung panggil webdriver tanpa Service Manager
    driver = webdriver.Chrome(options=chrome_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        # 1. CEK IP
        driver.get("https://api.ipify.org")
        ip_addr = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text
        print_log(f">>> IP BROWSER (TOR): {ip_addr}")
        print_log("-" * 40)

        # 2. LOAD MORE DARI PROFIL
        profile_url = "https://www.febspot.com/heru01221996"
        print_log(f">>> Mengecek profil: {profile_url}")
        driver.get(profile_url)
        time.sleep(7)

        last_count = 0
        same_count_retry = 0
        for i in range(25):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/video/')]")
            current_count = len(set([el.get_attribute("href") for el in elements if el.get_attribute("href")]))
            
            if current_count == last_count:
                same_count_retry += 1
                if same_count_retry >= 3: break
            else:
                same_count_retry = 0
            last_count = current_count

            try:
                load_more_btn = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Load more')]")))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_btn)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", load_more_btn)
                time.sleep(6)
            except:
                break

        scraped_links = [el.get_attribute("href") for el in driver.find_elements(By.XPATH, "//a[contains(@href, '/video/')]")]
        all_links = list(set(video_links + scraped_links))
        
        random.shuffle(all_links) 
        final_list = all_links[:100] 
        
        print_log(f">>> TOTAL DITEMUKAN: {len(all_links)} video.")
        print_log(f">>> BOT AKAN MEMUTAR: {len(final_list)} video acak.")
        print_log("-" * 40)

        # 3. MULAI NONTON
        for index, link in enumerate(final_list):
            print_log(f"[{index+1}/{len(final_list)}] Membuka: {link}")
            driver.get(link)
            time.sleep(5) 
            
            try:
                wait = WebDriverWait(driver, 25)
                video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                
                actions = ActionChains(driver)
                actions.move_to_element(video_element).click().perform()

                duration = driver.execute_script("return arguments[0].duration;", video_element)
                if duration and duration > 0:
                    # Kita batasi nonton 120 detik (2 menit) saja biar hemat kredit CircleCI
                    watch_time = min(int(duration), 120)
                    print_log(f"Nonton selama {watch_time} detik.")
                    time.sleep(watch_time)
                else:
                    time.sleep(25)
                print_log("✅ Selesai.")
            except Exception:
                print_log("❌ Gagal memuat video.")
            
            time.sleep(random.randint(4, 7))

    except Exception as e:
        print_log(f"⚠️ ERROR: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
