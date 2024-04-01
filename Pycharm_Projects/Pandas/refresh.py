from selenium import webdriver
import time

chrome_driver_path = r'C:\Users\Sightspectrum\Downloads\chromedriver_win32\chromedriver.exe'

driver = webdriver.Edge()

driver.get("https://www.google.com")

time.sleep(5)
driver.refresh()

driver.quit()

