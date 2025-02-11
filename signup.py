from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import time

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
    return ''.join(random.choice(characters)for _ in range(8))

# 랜덤 문자열 생성 함수(이름용, 한글 3글자)
def generate_random_korean_name():
    korean_start = 0xAC00  # "가"
    korean_end = 0xD558   # "하"
    return ''.join(chr(random.randint(korean_start, korean_end))for _ in range(3))

# 랜덤 비밀번호 생성 함수(영문, 숫자, 특수문자 조합)
def generate_random_password():
    letters = string.ascii_letters #영문
    digites = string.digits # 숫자
    special_chars = "!@#$%^&" # 사용할 특수문자
    all_chars = letters + digites + special_chars

    #최소 하나씩 포함하도록 보장
    password = [random.choice(letters), random.choice(digites), random.choice(special_chars)]
    #나머지 비밀번호 채우기
    password += [random.choice(all_chars) for _ in range(9)]
    #비밀번호 랜덤하게 섞기
    random.shuffle(password)
    return ''.join(password)

# 랜덤 연락처 생성 함수(숫자)
def generate_random_contact():
    fixed_prefix = "" # 앞자리 고정
    return fixed_prefix 

# 랜덤 이메일 생성 함수(영어 + 숫자)
def generate_random_email():
    prefix = ''.join(random.choice(string.ascii_letters + string.digits)for _ in range(5))
    domain = "seowoninfo.com"
    return f"{prefix}@{domain}"
    
# 공통 요소 함수
def wait_and_click(driver, by, value):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value))).click()

def wait_and_send_keys(driver, by, value, keys):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value))).send_keys(keys)

# 승인 버튼 클릭 함수(팝업 처리 포함)
def click_approval_buttons(drvier):
    try:
        #첫번째 승인 버튼 클릭
        wait_and_click(drvier, By.XPATH, "//button[@type='button' and span[text()='승인']]")
        print("첫 번째 승인 버튼 클릭 성공")
        
        #팝업 내부 승인 버튼 감지
        approval_button_xpath = ("//div[contains(@class, 'px-4 py-5')]//button[@type='button']//span[text()='승인']")
        approval_button = WebDriverWait(drvier, 10).until(EC.element_to_be_clickable((By.XPATH, approval_button_xpath)))
        print(f"승인 버튼 상태 : 표시됨={approval_button.is_displayed()}, 활성화됨={approval_button.is_enabled()}")
        #승인 버튼 클릭
        try:
            approval_button.click()
            print("승인 버튼 클릭 성공")
        except Exception as e:
            print(f"기본 클릭 실패 : {e}. javascript 강제 클릭 시도중")
            driver.execute_script("arguments[0].click();", approval_button)
            print("javascript 강제클릭성공")
    except Exception as e:
        print("실패")
 
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
    wait_and_click(driver, By.XPATH, "//button[@type='button' and span[text()='중복 확인']]")
    print("중복 확인 버튼 클릭 성공")

    # 조직 선택 버튼 클릭
    wait_and_click(driver, By.XPATH, "//button[@type='button' and span[text()='조직 선택']]")
    print("조직 선택 버튼 클릭 성공")

    # 조직 선택 완료
    wait_and_click(driver, By.XPATH, "//div[@class='flex flex-nowrap items-center rounded-md py-0.5']//span[@class='truncate' and text()='크리에이티브팀(수)a']")
    print("조직 선택 완료 성공")

    # 랜덤 이름 생성 및 입력
    random_name = generate_random_korean_name()
    wait_and_send_keys(driver, By.ID, "v-0-7", random_name)
    print(f"이름 입력 성공 : {random_name}")

    # 랜덤 비밀번호 생성 및 입력
    random_password = generate_random_password()
    wait_and_send_keys(driver, By.XPATH, "//input[@name='password']", random_password)
    wait_and_send_keys(driver, By.XPATH, "//input[@name='passwordRe']", random_password)
    print(f"비밀번호 입력 성공 : {random_password}")

    # 랜덤 연락처 및 이메일 생성
    #random_contact_information = "010" + ''.join(random.choice(string.digits) for _ in range(8))
    random_email = generate_random_email()
    #wait_and_send_keys(driver, By.XPATH, "//input[@name='phoneNumber']", random_contact_information)
    wait_and_send_keys(driver, By.XPATH, "//input[@name='email']", random_email)
    #print(f"연락처 및 이메일 입력 성공 : {random_contact_information}, {random_email}")

    # 회원가입 버튼 클릭
    wait_and_click(driver, By.XPATH, "//button[@type='submit' and span[text()='회원 가입']]")
    print("회원가입 버튼 클릭 성공")

    # 팝업 확인 버튼 클릭
    wait_and_click(driver, By.XPATH, "//button[@type='button' and span[text()='확인']]")
    print("확인 버튼 클릭 성공")

    # 관리자 로그인
    admin_id = "lshadmin"
    admin_password = "123qwe!@"
    wait_and_send_keys(driver, By.ID, "id", admin_id)
    wait_and_send_keys(driver, By.ID, "password", admin_password)
    wait_and_click(driver, By.XPATH, "//button[@type='submit']")
    print("관리자 계정 로그인 성공")

    # 클러스터 목록 및 환경설정
    wait_and_click(driver, By.XPATH, "//div[contains(@class, 'text-center') and contains(@class, 'relative')]")
    wait_and_click(driver, By.XPATH, "//button[@type='button']//span[contains(text(), '환경설정')]")
    print("환경설정 선택 성공")

    # 계정 관리
    wait_and_click(driver, By.XPATH, "//div[contains(text(), '계정 관리')]")
    wait_and_click(driver, By.XPATH, "//span[contains(text(), '가입 요청된 계정')]")
    wait_and_click(driver, By.XPATH, "//td//span")
    wait_and_click(driver, By.XPATH, "//input[@type='checkbox']")
   # 승인 버튼 클릭 (팝업 포함)
    click_approval_buttons(driver)
    print("✅ 가입 요청 승인 완료")


    #관리자 계정 로그아웃
    login_icon = driver.find_element(By. XPATH, "//button[@type='button']//span[contains(@class, 'i-bi:person-circle')]")
    # JavaScript로 클릭 강제 실행
    driver.execute_script("arguments[0].click()", login_icon)
    wait_and_click(driver, By.XPATH, "//span[contains(text(), '로그아웃')]")
    wait_and_click(driver, By.XPATH, "//span[contains(text(), '확인')]")
    print("✅ 관리자 계정 로그아웃 완료")
    
    #회원가입한 계정 정보 저장
    signed_up_id = random_id
    signed_up_password = random_password

    #회원가입한 계정으로 로그인
    wait_and_send_keys(driver, By.ID, "id", signed_up_id)
    wait_and_send_keys(driver, By.ID, "password", signed_up_password)
    wait_and_click(driver, By.XPATH, "//button[@type='submit']")
    print("✅ 회원가입한 계정 로그인 성공")

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    input("Enter 키를 눌러 브라우저를 종료하세요.")
