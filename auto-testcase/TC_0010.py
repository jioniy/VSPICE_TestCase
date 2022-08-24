# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import os
import inspect
import login_info as li
import default_url

tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"회원가입 시 모든 조건을 충족하는 경우 사용자 등록 버튼이 활성화되고, 회원가입 성공 시 로그인 화면으로 전환되어야 한다. "

class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_untitled_test_case(self):
        global test_details
        test_details = ''
        user_id = 'admin'
        user_pw = 'suresoft'
        
        driver = self.driver
        wait = WebDriverWait(driver, 600)
        driver.get(default_url.VSPICE_URL + "login")
        time.sleep(3)

        print("STEP 1 -- 회원가입 페이지 접속")
        driver.find_element_by_id("signUp").click()
        driver.get(default_url.VSPICE_URL + "UserRegister?")
        time.sleep(3)
        
        print("STEP 2 -- 회원가입 버튼 활성화 검사")
        #아이디 입력
        driver.find_element_by_xpath("//input[@type='text']").click()
        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("test100")
        time.sleep(1)
        #이름 입력
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[2]/div[2]/input").click()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[2]/div[2]/input").clear()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[2]/div[2]/input").send_keys("name100")
        time.sleep(1)
        #이메일 입력
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").click()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").clear()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").send_keys("email100@naver.com")
        time.sleep(1)
        #비밀번호 입력
        driver.find_element_by_xpath("//input[@type='password']").click()
        driver.find_element_by_xpath("//input[@type='password']").clear()
        driver.find_element_by_xpath("//input[@type='password']").send_keys("1q2w3e!!")
        time.sleep(1)
        #비밀번호 확인 입력
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[2]/div[2]/input").click()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[2]/div[2]/input").clear()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[2]/div[2]/input").send_keys("1q2w3e!!")
        time.sleep(2)
        #버튼 활성화 및 클릭 시 로그인 화면 이동
        element_btn = driver.find_element_by_id("userManageRegister-saveBtn")
        if element_btn.get_attribute("disabled") == None:
            print("STEP 2 -- SUCCESS")
        elif element_btn.get_attribute("disabled") == true:
            test_details += u"모든 항목이 충족해도 버튼이 활성화되지 않음\n"
        time.sleep(2)
        
        print("STEP 3 -- 회원가입 모달 검사")
        driver.find_element_by_id("userManageRegister-saveBtn").click()
        wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
        element = driver.find_element_by_id("modal-content")
        
        if element.text != u"회원가입이 완료되었습니다.":
            test_details += u"회원가입 실패\n"
        else:
            print("STEP3 -- SUCCESS")

        if (test_details != ''):
            assert False

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def tearDown(self):
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self.defaultTestResult()  # these 2 methods have no side effects
            self._feedErrorsToResult(result, self._outcome.errors)
        else:  # Python 3.2 - 3.3 or 3.0 - 3.1 and 2.7
            result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)
        #로그인
        li.login(self, "admin", "suresoft")
        #회원 삭제
        li.delete_user(self, "test100")
        
        error = self.list2reason(result.errors)
        failure = self.list2reason(result.failures)
        ok = not error and not failure

        if ok:
            test_result = 'SUCCESS'
        else:
            test_result = 'FAILURE'
            typ, text = ('ERROR', error) if error else ('FAIL', failure)
            text = text.replace('\"', '\'')

  
        data = '"' + tc_num + '"' + ',' + '"' + tc_content + '"' + ',' + '"' + test_result + '"' + ',' + '"' + test_details + '"'
        command = 'echo ' + data + ' >> vspice_test_result.csv'
        '''print(command)'''
        #os.system(command.encode(str('cp949')))
        os.system(command)
    
    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]
    
if __name__ == "__main__":
    unittest.main()