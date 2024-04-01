from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

chrome_driver_path = r'C:\Users\Sightspectrum\Downloads\chromedriver_win32\chromedriver.exe'

driver = webdriver.Edge()

driver.get("https://www.google.com")

search_box = driver.find_element(By.XPATH,'//*[@name="q"]')
search_box.send_keys("python")

search_box.send_keys(Keys.RETURN)

time.sleep(5)

# Find and click the first link in the search results
first_link = driver.find_element(By.XPATH, '//h3[@class="t"]/a')
first_link.click()

# Wait for a few seconds to let the page load
time.sleep(5)


print("Page Title:", driver.title)

driver.quit()

