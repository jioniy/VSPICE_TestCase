# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import os
import inspect
import default_url

tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"회원가입 시 이메일에 '@'문자가 없거나 한글이 들어가는 경우 '이메일 형식이 유효하지 않습니다.'라는 문구가 출력되어야 한다."

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
        
        driver = self.driver
        driver.get(default_url.VSPICE_URL + "login")
        time.sleep(2)
        
        print("STEP 1 -- 회원가입 페이지 접속")
        driver.find_element_by_id("signUp").click()
        driver.get(default_url.VSPICE_URL + "UserRegister?")
        time.sleep(2)
        
        print("STEP 2 -- 아이디 형식 검사 (@ 미입력)")
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").click()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").clear()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").send_keys("qw1234naver.com")
        time.sleep(2)
        
        element = driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[1]/div[3]/div[2]/div").text
        if(element!=u"이메일 형식이 유효하지 않습니다."):
            test_details += u"이메일에 '@' 미입력 시 이메일 형식 유효 메세지가 뜨지 않음\n"
        else:
            print("STEP 2 -- SUCCESS")
            
        print("STEP 3 -- 아이디 형식 검사 (@ 뒤 문자 미입력)")
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").click()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").clear()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").send_keys("qw1234@")
        time.sleep(2)
        
        element = driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[1]/div[3]/div[2]/div").text
        if(element!=u"이메일 형식이 유효하지 않습니다."):
            test_details += u"이메일에 '@' 뒤 문자 미입력 시 이메일 형식 유효 메세지가 뜨지 않음\n"
        else:
            print("STEP 3 -- SUCCESS")
            
        print("STEP 4 -- 아이디 형식 검사 (한글 입력)")
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").click()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").clear()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div/div[3]/div[2]/input").send_keys("ㅁㅁㅁ@naver.com")
        time.sleep(2)
        
        element = driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[1]/div[3]/div[2]/div").text
        if(element!=u"이메일 형식이 유효하지 않습니다."):
            test_details += u"이메일에 한글 입력 시 이메일 형식 유효 메세지가 뜨지 않음\n"
        else:
            print("STEP 4 -- SUCCESS")
            
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
