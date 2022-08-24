# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import login_info as li
import unittest, time, re
import os
import inspect

tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"프로젝트의 SCM 정보가 잘못 입력되었을 경우,  SCM 정보 오류에 관한 문구가 출력되어야 한다."

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
        
        li.login(self, "admin","suresoft")

        #프로젝트 등록 버튼
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_wrapper']/div/button/span").click()
        
        scm_url="http://vpes@192.168.0.136:7990/scm/sprin/vpes.git"
        scm_id="1212"
        scm_pw="1212"

        print("STEP 1 -- SCM GIT 인증 오류")
        #scm url 등록
        driver.find_element_by_id("projectCreate-scmUrl").click()
        driver.find_element_by_id("projectCreate-scmUrl").clear()
        driver.find_element_by_id("projectCreate-scmUrl").send_keys(scm_url)
        #scm id 등록
        driver.find_element_by_id("projectCreate-scmID").click()
        driver.find_element_by_id("projectCreate-scmID").clear()
        driver.find_element_by_id("projectCreate-scmID").send_keys(scm_id)
        #scm pw 등록
        driver.find_element_by_id("projectCreate-scmPW").click()
        driver.find_element_by_id("projectCreate-scmPW").clear()
        driver.find_element_by_id("projectCreate-scmPW").send_keys(scm_pw)
        time.sleep(1)
        #scm 인증
        driver.find_element_by_id("projectCreate-scmAuthBtn").click()
        
        #ajax return 값 대기 
        wait = WebDriverWait(driver, 15)
        element_text=""
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
            element_text = driver.find_element_by_id("modal-content").text
        except Exception as e:
            print(e)
        time.sleep(1)
        if element_text != u"SCM 계정정보를 설정해주세요.":
            print("STEP 1 -- FAILED")
            test_details += u"SCM GIT 인증에 실패했지만, 모달 알림이 뜨지 않음."
        else:
            print("STEP 1 -- SUCCESS")

        time.sleep(3)
        
        
        print("STEP 2 -- SCM SVN 인증 오류")
        driver.find_element_by_xpath("//div[@id='projectCreate-basicOpt']/div/div/div[2]/div/div/div[2]").click()
        driver.find_element_by_xpath("//div[@id='projectCreate-basicOpt']/div/div/div[2]/div/div/div[3]/ul/li[2]/span").click()
        time.sleep(1)
        #scm url 등록
        driver.find_element_by_id("projectCreate-scmUrl").click()
        driver.find_element_by_id("projectCreate-scmUrl").clear()
        driver.find_element_by_id("projectCreate-scmUrl").send_keys(scm_url)
        #scm id 등록
        driver.find_element_by_id("projectCreate-scmID").click()
        driver.find_element_by_id("projectCreate-scmID").clear()
        driver.find_element_by_id("projectCreate-scmID").send_keys(scm_id)
        #scm pw 등록
        driver.find_element_by_id("projectCreate-scmPW").click()
        driver.find_element_by_id("projectCreate-scmPW").clear()
        driver.find_element_by_id("projectCreate-scmPW").send_keys(scm_pw)
        time.sleep(1)
        #scm 인증
        driver.find_element_by_xpath("//button[@id='projectCreate-scmAuthBtn']/div").click()
        
        #ajax return 값 대기 
        wait = WebDriverWait(driver, 15)
        element_text=""
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
            element_text = driver.find_element_by_id("modal-content").text
        except Exception as e:
            print(e)
        time.sleep(1)
        if element_text != u"경로가 존재하지 않거나 접근 권한이 없습니다.":
            print("STEP 2 -- FAILED")
            test_details += u"SCM SVN 인증에 실패했지만, 모달 알림이 뜨지 않음."
        else:
            print("STEP 2 -- SUCCESS")

        time.sleep(3)
        
        print("STEP 3 -- SCM DIRECTORY 인증 오류")
        driver.find_element_by_xpath("//div[@id='projectCreate-basicOpt']/div/div/div[2]/div/div/div[2]").click()
        driver.find_element_by_xpath("//div[@id='projectCreate-basicOpt']/div/div/div[2]/div/div/div[3]/ul/li[3]/span").click()
        time.sleep(1)
            
        #scm url 등록
        driver.find_element_by_id("projectCreate-scmUrl").click()
        driver.find_element_by_id("projectCreate-scmUrl").clear()
        driver.find_element_by_id("projectCreate-scmUrl").send_keys(scm_url)
        time.sleep(1)
        
        #scm 인증
        driver.find_element_by_xpath("//button[@id='projectCreate-scmAuthBtn']/div").click()
        
        #ajax return 값 대기 
        wait = WebDriverWait(driver, 15)
        element_text=""
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
            element_text = driver.find_element_by_id("modal-content").text
        except Exception as e:
            print(e)
        time.sleep(1)
        if element_text != u"유효하지 않은 경로입니다.":
            print("STEP 3 -- FAILED")
            test_details += u"SCM DIRECTORY 인증에 실패했지만, 모달 알림이 뜨지 않음."
        else:
            print("STEP 3 -- SUCCESS")

        time.sleep(3)
    
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
