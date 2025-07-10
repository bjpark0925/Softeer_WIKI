from selenium import webdriver
from selenium.webdriver.chrome.service import Service

print("Selenium 스크립트 시작...")

options = webdriver.ChromeOptions()

# headless 옵션 설정 (디버깅을 위해 주석 처리)
# options.add_argument('--headless')
options.add_argument("--no-sandbox")

# 브라우저 윈도우 사이즈
options.add_argument('--window-size=1920,1080')

# 사람처럼 보이게 하는 옵션들
options.add_argument("--disable-gpu")   # 가속 사용 x
options.add_argument("--lang=ko_KR")    # 가짜 플러그인 탑재
options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정

print("Chrome 옵션 설정 완료")

# 드라이버 위치 경로 입력
try:
    service = Service('./chromedriver.exe')
    print("Chrome 서비스 생성 완료")
    
    driver = webdriver.Chrome(service=service, options=options)
    print("Chrome 드라이버 초기화 완료")
    
    driver.get('https://google.com')
    print("Google 페이지 로드 완료")
    
    driver.implicitly_wait(3)
    driver.get_screenshot_as_file('capture_google.png')    # 화면캡처
    print("스크린샷이 성공적으로 저장되었습니다: capture_google.png")
    
except Exception as e:
    print(f"오류 발생: {e}")
    import traceback
    traceback.print_exc()
finally:
    try:
        driver.quit() # driver 종료
        print("드라이버 종료 완료")
    except:
        print("드라이버 종료 중 오류 (이미 종료되었을 수 있음)")
