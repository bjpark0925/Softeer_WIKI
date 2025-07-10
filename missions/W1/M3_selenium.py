import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. 다운로드 경로 설정
download_dir = os.path.abspath("Softeer_WIKI\missions\W1\downloads")
os.makedirs(download_dir, exist_ok=True)

# 2. 크롬 드라이버 설정
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # GUI 없이 실행
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chrome_options)

try:
    # 3. IMF 데이터 포털 접속 및 검색
    driver.get("https://data.imf.org/")
    wait = WebDriverWait(driver, 20)

    search_box = wait.until(EC.presence_of_element_located((By.ID, "keyword")))
    search_box.clear()
    search_box.send_keys("GDP current prices")
    search_box.submit()

    # 4. "World Economic Outlook" 클릭
    weo_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "World Economic Outlook")))
    weo_link.click()

    # 5. 새 페이지 로딩 대기
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])  # 새 창으로 전환

    # 6. 데이터 브라우저 iframe 진입
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "databrowser")))
    time.sleep(3)

    # 7. Export 버튼 클릭
    export_btn = wait.until(EC.element_to_be_clickable((By.ID, "ExportButton")))
    export_btn.click()

    # 8. Excel 다운로드 클릭
    excel_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'Excel')]")))
    excel_btn.click()

    print("⏳ Downloading Excel file from IMF...")

    # 9. 다운로드 완료 대기
    download_complete = False
    for _ in range(30):
        time.sleep(1)
        if any(f.endswith(".xlsx") for f in os.listdir(download_dir)):
            download_complete = True
            break

    if not download_complete:
        raise Exception("❌ Download timed out")

    # 10. 다운로드된 파일명 확인
    file_path = next(os.path.join(download_dir, f) for f in os.listdir(download_dir) if f.endswith(".xlsx"))
    print(f"✅ File downloaded: {file_path}")

finally:
    driver.quit()

# 11. Pandas로 처리
print("📊 Processing with pandas...")

df_raw = pd.read_excel(file_path)

# GDP 필터링
df_gdp = df_raw[df_raw["Subject Descriptor"] == "Gross domestic product, current prices"]
df_gdp = df_gdp.drop(columns=["Subject Descriptor", "Units", "Scale"], errors="ignore")

df_long = df_gdp.melt(id_vars=["Country"], var_name="Year", value_name="GDP_Billion_USD")
df_long["GDP_Billion_USD"] = pd.to_numeric(df_long["GDP_Billion_USD"], errors="coerce")
df_long = df_long.dropna()
df_long = df_long[df_long["Year"].astype(str).str.isnumeric()]
df_long["GDP_Billion_USD"] = df_long["GDP_Billion_USD"].round(2)

# 12. 결과 출력
df_2023 = df_long[df_long["Year"] == "2023"]
df_2023_high = df_2023[df_2023["GDP_Billion_USD"] >= 100]
print("\n🌍 Countries with GDP ≥ 100B USD in 2023:")
print(df_2023_high.sort_values(by="GDP_Billion_USD", ascending=False))

# 13. 저장
df_long.to_csv("imf_gdp_selenium.csv", index=False)
print("\n💾 Saved cleaned data to imf_gdp_selenium.csv")
