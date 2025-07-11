import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.imf.org/external/datamapper/NGDPD@WEO/OEMDC/ADVEC/WEOWORLD/CAN/AFG/ASM/AND/AIA')
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "dm-ranking-value"))
)

elements = driver.find_elements(By.CLASS_NAME, "dm-ranking-value")
gdp_data = []
for element in elements:
    row = element.find_elements(By.TAG_NAME, 'span')
    if row[0].text:
        gdp_data.append([row[0].text, row[1].text])

df = pd.DataFrame(gdp_data)
print(df.head())

driver.quit()
