from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#드라이브 설정
def setup_driver():
    driver = webdriver.Chrome()
    driver.get('https://cubex.seowoninfo.com/auth')
    driver.maximize_window()
    return driver

#공통 요소
def wait_and_click(driver, by, value):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value))).click()

def wait_and_send_keys(driver, by, value, keys):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value))).send_keys(keys)


#로그인
def login(driver, username, password):
    try:
        wait_and_send_keys(driver, By.ID, "id", username)
        wait_and_send_keys(driver, By.ID, "password", password)
        wait_and_click(driver, By.XPATH, "//button[@type='submit']")
        WebDriverWait(driver, 10).until(EC.url_contains('home'))
        print("로그인 성공")
    except Exception as e:
        print(f"로그인 실패 :{repr(e)}")
        raise

#로그아웃
def logout(driver):
    try:
        wait_and_click(driver, By.CSS_SELECTOR, "span.iconify.i-bi\\:person-circle")
        wait_and_click(driver, By.CSS_SELECTOR, "span.truncate")
        wait_and_click(driver, By.XPATH, "//button[@type='button' and span[text()='확인']]")
        WebDriverWait(driver, 10).until(EC.url_contains('auth'))
        print("로그아웃 성공")
    except Exception as e:
        print(f'로그아웃 실패{repr(e)}')
        raise

#로그인 실패
def test_login_failure(driver, username, password, test_type):
    try:
        wait_and_send_keys(driver, By.ID, "id", username)
        wait_and_send_keys(driver, By.ID, "password", password)
        wait_and_click(driver, By.XPATH, "//button[@type='submit']")
        wait_and_click(driver, By.XPATH, "//button[@type='button' and span[text()='확인']]")
        WebDriverWait(driver, 10).until(EC.url_contains('auth'))
        print(f"로그인 실패 테스트 성공 : {test_type}")
    except Exception as e:
        print(f'테스트 실패{repr(e)}')
        raise
#메인 실행
def main():
    driver = setup_driver()
    
    try:
        login(driver, "lshadmin", "123qwe!@")
        logout(driver)
    # 아이디 오입력
        test_login_failure(driver, "lshaadmin", "123qwe!@", "아이디 오입력" )
    # 비밀번호 오입력
        test_login_failure(driver, "lshadmin", "1234qwe!@", "비밀번호 오입력" )
    
    except Exception as e:
        print(f"테스트 실패{repr(e)}")
    
if __name__ == "__main__":
    main()







