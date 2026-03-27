from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random
import urllib.parse
from datetime import datetime, timedelta

def connect_and_scrape_safe(keywords, gun_sayisi=30):
    results = []
    
    bitis = datetime.now().strftime('%Y-%m-%d')
    baslangic = (datetime.now() - timedelta(days=gun_sayisi)).strftime('%Y-%m-%d')
    
    print(f"--- TWITTER TARAMASI BAŞLIYOR ({baslangic} ile {bitis} arası) ---")
    print("NOT: Chrome'un 9222 portuyla açık olduğundan emin olun.")
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("✓ Mevcut Chrome penceresine bağlanıldı.")
        
        for index, word in enumerate(keywords):
            print(f"[{index+1}/{len(keywords)}] --> '{word}' aranıyor...")
            
            try:
                query = f"{word} lang:tr since:{baslangic} until:{bitis}"
                encoded_query = urllib.parse.quote(query)
                search_url = f"https://twitter.com/search?q={encoded_query}&src=typed_query&f=live"
                
                driver.get(search_url)
                
                time.sleep(random.uniform(5, 8))
                
                found_tweets_in_loop = set()
                scroll_count = 30 # Tarih aralığı genişse bu sayıyı artırabilirsiniz
                
                for i in range(scroll_count):
                    tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                    
                    for t in tweets:
                        try:
                            text = t.text
                            if len(text) > 20 and text not in found_tweets_in_loop:
                                results.append({
                                    "Tarih Aralığı": f"{baslangic}/{bitis}",
                                    "Konu": word,
                                    "Tweet": text
                                })
                                found_tweets_in_loop.add(text)
                        except:
                            continue
                    
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random.uniform(3, 5))
                
                print(f"    ✓ Bu kelime için {len(found_tweets_in_loop)} tweet bulundu.")
                
            except Exception as e:
                print(f"    ! Hata oluştu: {e}")
            
            if index < len(keywords) - 1:
                bekleme = random.uniform(6, 12)
                print(f"    (Güvenlik molası: {int(bekleme)} sn...)\n")
                time.sleep(bekleme)

    except Exception as e:
        print(f"\n!!! BAĞLANTI HATASI: {e}")
    
    finally:
        print("\n--- İŞLEM TAMAMLANDI ---")
        if results:
            df = pd.DataFrame(results)
            dosya_adi = f"twitter_analiz_{datetime.now().strftime('%d_%m_%Y')}.xlsx"
            df.to_excel(dosya_adi, index=False)
            print(f"Rapor oluşturuldu: {dosya_adi}")
            print(f"Toplam çekilen veri: {len(df)}")
        else:
            print("Veri çekilemedi.")

keywords = [
    "key word1",
    "keyword2"
]

if __name__ == "__main__":
    connect_and_scrape_safe(keywords, gun_sayisi=36)