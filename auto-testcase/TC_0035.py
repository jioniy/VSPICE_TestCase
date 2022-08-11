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
from login import login
from datetime import datetime, timedelta
import unittest, time, re
import os
import inspect
import project_info as pi

tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"ACQ4의 책무/합의 템플릿을 다운로드 받을 경우, 'ACQ4_02-01_책무 합의.xlsx'파일이 다운로드 되어야 한다. "

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
        
        project_name = "TC_0035"
        
        user_id = "admin"
        user_pw = "suresoft"
        
        print("STEP 1 -- 프로젝트 세팅")
        
        print("STEP 1-1 -- 사용자 로그인 및 프로젝트 등록")
        login(self, user_id, user_pw)
        
        # 프로젝트 생성
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "VPES_CAR")
        test_details += pi.project_process_info(self, True, True, True, True, True, True, True, True, True, True, True, True, True) # MAN 프로세스에 승인 요청 기능 사용
        test_details += pi.create_project(self)
        
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속")
        pi.search_project(self, project_name)
        
        print("STEP 2 -- 프로세스 승인 요청 문구 확인")
        print("STEP 2-1 -- ACQ 프로세스 승인 요청 문구 확인")
        driver.find_element_by_id("processes-tab").click()
        driver.find_element_by_id("acq").click()
        time.sleep(3)
        element_text = driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div/div[2]").text
        if element_text == "작업 산출물 승인 요청 사용 중":
            print("STEP 2-1 -- SUCCESS")
        else:
            print("STEP 2-1 -- FAILED")
            test_details += u"ACQ 프로세스가 승인 요청 기능을 사용하지만, 프로세스 상세 페이지에 표시되지 않음\n"
        
        print("STEP 2-2 -- MAN 프로세스 승인 요청 문구 확인")
        driver.find_element_by_id("man").click()
        time.sleep(3)
        element_text = driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div/div[2]").text
        if element_text == "작업 산출물 승인 요청 사용 중":
            print("STEP 2-2 -- SUCCESS")
        else:
            print("STEP 2-2 -- FAILED")
            test_details += u"MAN 프로세스가 승인 요청 기능을 사용하지만, 프로세스 상세 페이지에 표시되지 않음\n"
        
        print("STEP 2-3 -- SYS 프로세스 승인 요청 문구 확인")
        driver.find_element_by_id("sys").click()
        time.sleep(3)
        element_text = driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div/div[2]").text
        if element_text == "작업 산출물 승인 요청 사용 중":
            print("STEP 2-3 -- SUCCESS")
        else:
            print("STEP 2-3 -- FAILED")
            test_details += u"SYS 프로세스가 승인 요청 기능을 사용하지만, 프로세스 상세 페이지에 표시되지 않음\n"
        
        print("STEP 2-4 -- SWE 프로세스 승인 요청 문구 확인")
        driver.find_element_by_id("swe").click()
        time.sleep(3)
        element_text = driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div/div[2]").text
        if element_text == "작업 산출물 승인 요청 사용 중":
            print("STEP 2-4 -- SUCCESS")
        else:
            print("STEP 2-4 -- FAILED")
            test_details += u"SWE 프로세스가 승인 요청 기능을 사용하지만, 프로세스 상세 페이지에 표시되지 않음\n"
            
        print("STEP 2-5 -- SUP 프로세스 승인 요청 문구 확인")
        driver.find_element_by_id("sup").click()
        time.sleep(3)
        element_text = driver.find_element_by_xpath("//div[@id='processDetail-ReportVue']/div/div[2]").text
        if element_text == "작업 산출물 승인 요청 사용 중":
            print("STEP 2-5 -- SUCCESS")
        else:
            print("STEP 2-5 -- FAILED")
            test_details += u"SUP 프로세스가 승인 요청 기능을 사용하지만, 프로세스 상세 페이지에 표시되지 않음\n"
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
            
        pi.delete_project(self, "TC_0035")
        
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
        command = 'echo ' + data + ' >> vpes_test_result.csv'
        '''print(command)'''
        #os.system(command.encode(str('cp949')))
        os.system(command)
    
    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]
    
if __name__ == "__main__":
    unittest.main()
