import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import time

# ✅ Chromedriver 자동 설치
chromedriver_autoinstaller.install()

# ✅ Chrome 옵션 설정 (Headless 모드 추가)
chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드 (GUI 없이 실행)
chrome_options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화 (CI/CD 환경에서 필요)
chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 문제 해결
chrome_options.add_argument("--window-size=1920x1080")  # 화면 크기 설정
chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화 (리눅스 환경에서 필요)

# ✅ WebDriver 실행 (헤드리스 모드 적용)
driver = webdriver.Chrome(options=chrome_options)

# ✅ 웹사이트 이동
driver.get('https://cubex.seowoninfo.com/auth')
driver.maximize_window()

# 랜덤 문자열 생성 함수(아이디용)
def generate_random_string():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

# 랜덤 문자열 생성 함수(이름용, 한글 3글자)
def generate_random_korean_name():
    korean_start = 0xAC00  # "가"
    korean_end = 0xD7A3   # "힣"
    return ''.join(chr(random.randint(korean_start, korean_end)) for _ in range(3))

# 랜덤 비밀번호 생성 함수(영문, 숫자, 특수문자 조합)
def generate_random_password():
    letters = string.ascii_letters
    digits = string.digits
    special_chars = "!@#$%^&"
    all_chars = letters + digits + special_chars

    # 최소 하나씩 포함하도록 보장
    password = [random.choice(letters), random.choice(digits), random.choice(special_chars)]
    # 나머지 비밀번호 채우기
    password += [random.choice(all_chars) for _ in range(9)]
    # 비밀번호 랜덤하게 섞기
    random.shuffle(password)
    return ''.join(password)

# 랜덤 이메일 생성 함수(영어 + 숫자)
def generate_random_email():
    prefix = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    domain = "seowoninfo.com"
    return f"{prefix}@{domain}"
    
# 공통 요소 함수
def wait_and_click(driver, by, value):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value))).click()

def wait_and_send_keys(driver, by, value, keys):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value))).send_keys(keys)

# 승인 버튼 클릭 함수(팝업 처리 포함)
def click_approval_buttons(driver):
    try:
        # 첫 번째 승인 버튼 클릭
        wait_and_click(driver, By.XPATH, "//button[@type='button']//span[contains(text(), '승인')]")
        print("첫 번째 승인 버튼 클릭 성공")
        
        # 팝업 내부 승인 버튼 감지
        approval_button_xpath = "//div[contains(@class, 'px-4 py-5')]//button[@type='button']//span[contains(text(), '승인')]"
        approval_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, approval_button_xpath)))
        
        # 승인 버튼 클릭
        try:
            approval_button.click()
            print("승인 버튼 클릭 성공")
        except Exception as e:
            print(f"기본 클릭 실패 : {e}. JavaScript 강제 클릭 시도 중")
            driver.execute_script("arguments[0].click();", approval_button)
            print("JavaScript 강제 클릭 성공")
    except Exception as e:
        print(f"승인 버튼 클릭 실패: {e}")

try:
    # 회원가입 버튼 클릭
    wait_and_click(driver, By.XPATH, "//a[@href='/auth/sign-up']")
    WebDriverWait(driver, 10).until(EC.url_contains('sign-up'))
    print("회원가입 버튼 클릭 성공")

    # 랜덤 아이디 생성 및 입력
    random_id = generate_random_string().lower()
    wait_and_send_keys(driver, By.ID, "v-0-5", random_id)
    print(f"랜덤 아이디 입력 성공: {random_id}")

    # 중복확인 버튼 클릭
    wait_and_click(driver, By.XPATH, "//button[@type='button']//span[contains(text(), '중복 확인')]")
    print("중복 확인 버튼 클릭 성공")

    # 조직 선택 버튼 클릭
    wait_and_click(driver, By.XPATH, "//button[@type='button']//span[contains(text(), '조직 선택')]")
    print("조직 선택 버튼 클릭 성공")

    # 조직 선택 완료
    wait_and_click(driver, By.XPATH, "//span[contains(text(), '크리에이티브팀(수)a')]")
    print("조직 선택 완료 성공")

    # 랜덤 이름 생성 및 입력
    random_name = generate_random_korean_name()
    wait_and_send_keys(driver, By.ID, "v-0-7", random_name)
    print(f"이름 입력 성공: {random_name}")

    # 랜덤 비밀번호 생성 및 입력
    random_password = generate_random_password()
    wait_and_send_keys(driver, By.XPATH, "//input[@name='password']", random_password)
    wait_and_send_keys(driver, By.XPATH, "//input[@name='passwordRe']", random_password)
    print(f"비밀번호 입력 성공: {random_password}")

    # 랜덤 이메일 생성 및 입력
    random_email = generate_random_email()
    wait_and_send_keys(driver, By.XPATH, "//input[@name='email']", random_email)
    print(f"이메일 입력 성공: {random_email}")

    # 회원가입 버튼 클릭
    wait_and_click(driver, By.XPATH, "//button[@type='submit']//span[contains(text(), '회원 가입')]")
    print("회원가입 버튼 클릭 성공")

    # 팝업 확인 버튼 클릭
    wait_and_click(driver, By.XPATH, "//button[@type='button']//span[contains(text(), '확인')]")
    print("확인 버튼 클릭 성공")

    # 관리자 로그인
    admin_id = "lshadmin"
    admin_password = "123qwe!@"
    wait_and_send_keys(driver, By.ID, "id", admin_id)
    wait_and_send_keys(driver, By.ID, "password", admin_password)
    wait_and_click(driver, By.XPATH, "//button[@type='submit']")
    print("관리자 계정 로그인 성공")

    # 계정 승인 처리
    wait_and_click(driver, By.XPATH, "//span[contains(text(), '가입 요청된 계정')]")
    click_approval_buttons(driver)
    print("✅ 가입 요청 승인 완료")

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    driver.quit()
    print("✅ WebDriver 종료 완료")

