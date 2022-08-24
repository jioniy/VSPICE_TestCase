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
tc_content = u"회원가입 시 비밀번호가 공백이거나 문자, 숫자, 특수문자를 모두 포함하지 않는 경우 해당 문구가 출력되어야한다."

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
        
        print("STEP 2 -- 비밀번호 유효성 검사")
        print("STEP 2-1 -- 문자 미포함 검사")
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").click()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").clear()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").send_keys("1234567!")
        time.sleep(2)
        
        element = driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/div").text
        if(element!=u"비밀번호는 8자리 이상 문자, 숫자, 특수문자를 포함하며 공백이 없어야 합니다."):
            test_details += u"비밀번호 문자 미포함 시 메세지가 뜨지 않음\n"
        else:
            print("STEP 2-1 -- SUCCESS")
        time.sleep(2)
        
        print("STEP 2-2 -- 숫자 미포함 검사")
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").click()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").clear()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").send_keys("qwerasdf!")
        time.sleep(2)
        
        element = driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/div").text
        if(element!=u"비밀번호는 8자리 이상 문자, 숫자, 특수문자를 포함하며 공백이 없어야 합니다."):
            test_details += u"비밀번호 숫자 미포함 시 메세지가 뜨지 않음\n"
        else:
            print("STEP 2-2 -- SUCCESS")
        time.sleep(2)    
        
        print("STEP 2-3 -- 특수문자 미포함 검사")
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").click()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").clear()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").send_keys("qweras123")
        time.sleep(2)
        
        element = driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/div").text
        if(element!=u"비밀번호는 8자리 이상 문자, 숫자, 특수문자를 포함하며 공백이 없어야 합니다."):
            test_details += u"비밀번호 특수문자 미포함 시 메세지가 뜨지 않음\n"
        else:
            print("STEP 2-3 -- SUCCESS")
        time.sleep(2)
        
        
        print("STEP 3 -- 비밀번호 길이 검사")
        print("STEP 3-1 -- 8자 미충족 검사")
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").click()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").clear()
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").send_keys("qwer3!")
        time.sleep(2)
        
        element = driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/div").text
        if(element!=u"비밀번호는 8자리 이상 문자, 숫자, 특수문자를 포함하며 공백이 없어야 합니다."):
            test_details += u"비밀번호가 8자 미만일 때 메세지가 뜨지 않음\n"
        else:
            print("STEP 3-1 -- SUCCESS")
        
        
        print("STEP 3-2 -- 공백 검사")
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").send_keys(Keys.CONTROL + "a")
        driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/input").send_keys(Keys.DELETE)
        time.sleep(2)
        
        element = driver.find_element_by_xpath("//div[@id='userInfoVue']/div/div[3]/div[2]/div[1]/div[2]/div").text
        if(element!=u"비밀번호는 8자리 이상 문자, 숫자, 특수문자를 포함하며 공백이 없어야 합니다."):
            test_details += u"비밀번호가 공백일 때 메세지가 뜨지 않음\n"
        else:
            print("STEP 3-2 -- SUCCESS")
        
        
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
