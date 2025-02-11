import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ Chromedriver 자동 설치
chromedriver_autoinstaller.install()

# ✅ WebDriver 설정 (Headless 모드 추가)
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless 모드 활성화
    chrome_options.add_argument("--no-sandbox")  # 샌드박스 비활성화 (CI/CD 환경에서 필수)
    chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 문제 방지
    chrome_options.add_argument("--window-size=1920x1080")  # 브라우저 창 크기 설정
    chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화 (리눅스 환경에서 필요)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://cubex.seowoninfo.com/auth')
    driver.maximize_window()
    return driver

# ✅ 공통 요소
def wait_and_click(driver, by, value):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value))).click()

def wait_and_send_keys(driver, by, value, keys):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value))).send_keys(keys)

# ✅ 로그인
def login(driver, username, password):
    try:
        wait_and_send_keys(driver, By.ID, "id", username)
        wait_and_send_keys(driver, By.ID, "password", password)
        wait_and_click(driver, By.XPATH, "//button[@type='submit']")
        WebDriverWait(driver, 10).until(EC.url_contains('home'))
        print("✅ 로그인 성공")
    except Exception as e:
        print(f"❌ 로그인 실패 : {repr(e)}")
        raise

# ✅ 로그아웃
def logout(driver):
    try:
        # 로그아웃 버튼 클릭 (XPath 선택자 안정성 개선)
        logout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'logout-button')]"))
        )
        driver.execute_script("arguments[0].click();", logout_button)  # JavaScript 클릭 추가
        wait_and_click(driver, By.XPATH, "//span[contains(text(), '로그아웃')]")
        wait_and_click(driver, By.XPATH, "//span[contains(text(), '확인')]")
        WebDriverWait(driver, 10).until(EC.url_contains('auth'))
        print("✅ 로그아웃 성공")
    except Exception as e:
        print(f"❌ 로그아웃 실패 {repr(e)}")
        raise

# ✅ 로그인 실패 테스트
def test_login_failure(driver, username, password, test_type):
    try:
        wait_and_send_keys(driver, By.ID, "id", username)
        wait_and_send_keys(driver, By.ID, "password", password)
        wait_and_click(driver, By.XPATH, "//button[@type='submit']")
        wait_and_click(driver, By.XPATH, "//button[@type='button']//span[contains(text(), '확인')]")
        WebDriverWait(driver, 10).until(EC.url_contains('auth'))
        print(f"✅ 로그인 실패 테스트 성공: {test_type}")
    except Exception as e:
        print(f"❌ 로그인 실패 테스트 오류: {repr(e)}")
        raise

# ✅ 메인 실행
def main():
    driver = setup_driver()
    
    try:
        # 관리자 로그인 및 로그아웃
        login(driver, "lshadmin", "123qwe!@")
        logout(driver)

        # 로그인 실패 테스트
        test_login_failure(driver, "lshaadmin", "123qwe!@", "아이디 오입력")
        test_login_failure(driver, "lshadmin", "1234qwe!@", "비밀번호 오입력")
    
    except Exception as e:
        p









