from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random
import urllib.parse

def connect_and_scrape_safe(keywords):
    results = []
    
    print("--- GÜVENLİ MODDA TWITTER TARAMASI BAŞLIYOR ---")
    print("NOT: Chrome'un CMD üzerinden '9222' portuyla açık olması gerekir.")
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("✓ Mevcut Chrome penceresine başarıyla bağlanıldı.")
        
        for index, word in enumerate(keywords):
            print(f"[{index+1}/{len(keywords)}] --> '{word}' aranıyor...")
            
            try:
                query = f"{word} lang:tr"
                encoded_query = urllib.parse.quote(query)
                search_url = f"https://twitter.com/search?q={encoded_query}&src=typed_query&f=live"
                
                driver.get(search_url)
                
                time.sleep(random.uniform(4, 7))
                
                found_tweets_in_loop = set()
                scroll_count = 10 
                
                for i in range(scroll_count):
                    tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                    
                    for t in tweets:
                        try:
                            text = t.text
                            # Tekrar eden tweetleri ve çok kısa olanları alma
                            if len(text) > 20 and text not in found_tweets_in_loop:
                                results.append({
                                    "Konu": word,
                                    "Tweet": text
                                })
                                found_tweets_in_loop.add(text)
                        except:
                            continue
                    
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random.uniform(3, 6))
                
                print(f"    ✓ {len(found_tweets_in_loop)} tweet toplandı.")
                
            except Exception as e:
                print(f"    ! Arama sırasında hata: {e}")
            
            if index < len(keywords) - 1: # Son kelimede beklemesin
                wait_time = random.uniform(5, 10)
                print(f"    (Güvenlik için {int(wait_time)} saniye bekleniyor...)\n")
                time.sleep(wait_time)

    except Exception as e:
        print(f"\n!!! BAĞLANTI HATASI: {e}")
        print("ÇÖZÜM: Lütfen Chrome'u CMD'den '--remote-debugging-port=9222' komutuyla başlattığınızdan emin olun.")

    finally:
        print("\n--- İŞLEM BİTTİ ---")
        if results:
            df = pd.DataFrame(results)
            dosya_adi = "hazir_yemek_sikayet_analizi.xlsx"
            df.to_excel(dosya_adi, index=False)
            print(f"Rapor hazırlandı: {dosya_adi}")
            print(f"Toplam {len(df)} adet veri çekildi.")
        else:
            print("Veri bulunamadı veya bağlantı sağlanamadı.")

keywords = [
    "keyword1",
    "key word2"


]


if __name__ == "__main__":
    connect_and_scrape_safe(keywords)