import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import default_url
'''
login_info.py :: 사용자 로그인/로그아웃/회원가입/삭제 모듈
    - login() :: 로그인 
    - logout() :: 로그아웃
    - join() :: 회원가입
    - delete_user() :: 사용자 삭제 
return FAILED Message
'''
def login(self, id, pw):
    print(":: LOGIN :: 로그인")
    failed_messages=""
    driver=self.driver
    driver.get(default_url.VSPICE_URL + "login")
    time.sleep(2)
    driver.find_element_by_id("username").clear()
    driver.find_element_by_id("username").send_keys(id)
    time.sleep(1)
    driver.find_element_by_id("pwd").click()
    driver.find_element_by_id("pwd").clear()
    driver.find_element_by_id("pwd").send_keys(pw)
    time.sleep(1)
    driver.find_element_by_name("mform").submit()
    time.sleep(3)
    if driver.current_url== default_url.VSPICE_URL :
        print(":: LOGIN :: SUCCESS")
    else:
        print(":: LOGIN :: FAILED")
        failed_messages+=u"로그인 실패"
    return failed_messages
    
def logout(self):
    print(":: LOGOUT :: 로그아웃")
    driver = self.driver
    driver.find_element_by_id("TopNavBarUserInfoDropDownBtn").click()
    time.sleep(1)
    driver.find_element_by_link_text(u"로그아웃").click()
    time.sleep(3)
    
def join(self, user_id, user_name, user_email, user_pw, user_pw_ck):
    failed_messages=""
    print(":: JOIN :: 회원가입")
    driver = self.driver
    driver.get(default_url.VSPICE_URL +"login")
    
    print(":: JOIN - 회원가입 페이지 접속 ::")
    driver.find_element_by_id("signUp").click()
    driver.get(default_url.VSPICE_URL + "UserRegister?")
    time.sleep(3)
    
    print(":: JOIN - 필수 정보 입력 ::")
    #아이디 입력
    driver.find_element_by_xpath("//input[@type='text']").click()
    driver.find_element_by_xpath("//input[@type='text']").clear()
    driver.find_element_by_xpath("//input[@type='text']").send_keys(user_id)
    time.sleep(2)
    #이름 입력
    driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[2]/div[2]/input").click()
    driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[2]/div[2]/input").clear()
    driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[2]/div[2]/input").send_keys(user_name)
    time.sleep(2)
    #이메일 입력
    driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").click()
    driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").clear()
    driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").send_keys(user_email)
    time.sleep(2)
    #비밀번호 입력
    driver.find_element_by_xpath("//input[@type='password']").click()
    driver.find_element_by_xpath("//input[@type='password']").clear()
    driver.find_element_by_xpath("//input[@type='password']").send_keys(user_pw)
    time.sleep(2)
    #비밀번호 확인 입력
    driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[2]/div[2]/input").click()
    driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[2]/div[2]/input").clear()
    driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[2]/div[2]/input").send_keys(user_pw)
    time.sleep(3)
    
    #버튼 활성화 및 클릭 시 로그인 화면 이동
    element_btn = driver.find_element_by_id("userManageRegister-saveBtn")
    
    if element_btn.get_attribute("disabled") == None:
        element_btn.click()
    else:
        print(":: JOIN :: 사용자 등록 버튼 활성화 실패")
        
    wait = WebDriverWait(driver,10)
    wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
    element = driver.find_element_by_id("modal-content")
    
    if element.text != u"회원가입이 완료되었습니다.":
        print(":: JOIN :: FAILED")
        failed_messages += u"회원가입 실패\n"
    else:
        print(":: JOIN :: SUCCESS")
        
    return failed_messages
    
def delete_user(self, user_id): 
    # 해당 함수를 사용할 때 admin 사용자로 로그인된 상태라고 가정함. 
    failed_messages=""
    print(":: DELETE_USER :: 사용자 삭제 (" + user_id + ")")
    driver = self.driver
    
    #회원 삭제
    driver.get(default_url.VSPICE_URL)
    time.sleep(3)
    driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='프로젝트가 존재하지 않습니다.'])[1]/following::*[name()='svg'][1]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//div[@id='globalSettingUserList_filter']/label/input").click()
    driver.find_element_by_xpath("//div[@id='globalSettingUserList_filter']/label/input").clear()
    driver.find_element_by_xpath("//div[@id='globalSettingUserList_filter']/label/input").send_keys(user_id)
    time.sleep(2)
    driver.find_element_by_xpath("//div[@id='globalSettingUserList_filter']/label/input").send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element_by_id("userDelete").click()
    time.sleep(2)
    driver.find_element_by_id("deleteY").click()
    time.sleep(2)
    
    if driver.find_element_by_xpath("//tbody[@id='globalSettingUserContent']/tr/td").text=="검색할 데이터가 없습니다.":
        print(":: DELETE_USER :: SUCCESS")
    else:
        print(":: DELETE_USER :: FAILED")
        failed_messages += "회원삭제 실패\n"
    
    return failed_messages