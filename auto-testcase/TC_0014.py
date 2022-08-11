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


tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"프로젝트 일정의 시작일보다 종료일이 빠르거나 기간이 4년 이상일 경우,  '프로젝트 일정이 올바르지 않습니다.'라는 문구가 출력되어야 한다."

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
        
        login(self, "admin","suresoft")

        #프로젝트 등록 버튼
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_wrapper']/div/button/span").click()

        print("STEP 1 -- 프로젝트 일정의 시작일보다 종료일보다 빠른 경우")
        
       #프로젝트 기간 입력
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date_res = datetime.now()+timedelta(days=-1)
        end_date = end_date_res.strftime('%Y-%m-%d')
            
        driver.find_element_by_id("projectCreate-startDate").click()
        driver.find_element_by_id("projectCreate-startDate").click()
        driver.find_element_by_id("projectCreate-startDate").clear()
        time.sleep(1)
        driver.find_element_by_id("projectCreate-startDate").send_keys(start_date)
        time.sleep(1)
        driver.find_element_by_id("projectCreate-endDate").click()
        driver.find_element_by_id("projectCreate-endDate").click()
        driver.find_element_by_id("projectCreate-endDate").clear()
        time.sleep(1)
        driver.find_element_by_id("projectCreate-endDate").send_keys(end_date)
        time.sleep(1)
        
        element_text=driver.find_element_by_xpath("//div[@id='projectCreate-basicOpt']/div[4]/div[2]/div[4]/span").text
        if element_text!=u"프로젝트 일정이 올바르지 않습니다.":
            print("STEP 1 -- FAILED")
            test_details+=u"프로젝트 시작일보다 종료일이 빠르지만 문구가 뜨지 않음.\n"
        else:
            print("STEP 1 -- SUCCESS")
        
        time.sleep(1)
            
        print("STEP 2 -- 프로젝트 일정 기간이 4년 이상인 경우")
        
       #프로젝트 기간 입력
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date_res = datetime.now()+timedelta(days=1465)
        end_date = end_date_res.strftime('%Y-%m-%d')
            
        driver.find_element_by_id("projectCreate-startDate").click()
        driver.find_element_by_id("projectCreate-startDate").click()
        driver.find_element_by_id("projectCreate-startDate").clear()
        time.sleep(1)
        driver.find_element_by_id("projectCreate-startDate").send_keys(start_date)
        time.sleep(1)
        driver.find_element_by_id("projectCreate-endDate").click()
        driver.find_element_by_id("projectCreate-endDate").click()
        driver.find_element_by_id("projectCreate-endDate").clear()
        time.sleep(1)
        driver.find_element_by_id("projectCreate-endDate").send_keys(end_date)
        time.sleep(1)
        
        element_text=driver.find_element_by_xpath("//div[@id='projectCreate-basicOpt']/div[4]/div[2]/div[4]/span").text
        if element_text!=u"프로젝트 일정이 올바르지 않습니다.":
            print("STEP 2 -- FAILED")
            test_details+=u"프로젝트 기간이 4년 이상이지만 문구가 뜨지 않음.\n"
        else:
            print("STEP 2 -- SUCCESS")
            
            
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
        command = 'echo ' + data + ' >> vpes_test_result.csv'
        '''print(command)'''
        #os.system(command.encode(str('cp949')))
        os.system(command)
    
    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]
    
if __name__ == "__main__":
    unittest.main()
