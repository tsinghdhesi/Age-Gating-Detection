from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
import time  

service = Service(executable_path="chromedriver.exe")

options = Options()
options.add_argument('--no-sandbox')
options.add_argument("--headless")
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)

f = open("All-Site-Links.txt", "r")
count = 0
for url in f:
    print(url.strip())
    try:
        driver.get("https://www." + url.strip())
        time.sleep(8)
        name = 'Site-Images\\' + url.strip() + '.png'
        driver.save_screenshot(name)
        
    except WebDriverException as e:
        print("Site not found for " + url.strip())
        print("ERROR: ", e)
        
        # Try to search on Google if site is not found
        try:
            driver.get("https://www.google.com")
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
            )
            input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
            input_element.clear()
            input_element.send_keys(f'"{url.strip()}"' + Keys.ENTER)
            
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'h3'))
                )
                link = driver.find_element(By.CSS_SELECTOR, 'h3')
                link.click()
                time.sleep(8)
                name = 'Site-Images\\' + url.strip() + '.png'
                driver.save_screenshot(name)
                
            except TimeoutException:
                print("No URL found on Google for " + url.strip())
                count += 1
        except TimeoutException as e:
            print("Timeout occurred while searching for " + url.strip())
            print("ERROR: ", e)

    except TimeoutException as e:
        print("Timeout while trying to load site for " + url.strip())
        print("ERROR: ", e)

if count % 39 == 0:
    driver.quit()
    driver = webdriver.Chrome(service=service, options=options)

print("Total count of unfound URLs:", count)
f.close()
driver.quit()
