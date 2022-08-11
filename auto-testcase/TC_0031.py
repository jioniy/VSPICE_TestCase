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
tc_content = u"프로젝트 등록 시 설정한 프로세스에 해당하는 프로세스 항목만 존재해야 한다."

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
        print("STEP 1 -- 프로젝트 검색 및 클릭")
        project_name = "TC_0031"
        
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "VPES_CAR")
        test_details += pi.project_process_info(self, True, False, True, True, True, False, True, True)# MAN, SUP8 제외
        test_details += pi.create_project(self)
        
        #프로젝트 이름 검색
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").click()
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").clear()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").send_keys(project_name)
        driver.find_element_by_xpath("//div[@id='mainDashBoard-ProjectList_filter']/label/input").send_keys(Keys.ENTER)
        time.sleep(2)
        
        #해당 프로젝트 클릭
        driver.find_element_by_xpath("//table[@id='mainDashBoard-ProjectList']/tbody/tr/td[2]").click()
        time.sleep(2)
        
        
        # style= display none 속성으로 찾기 
        driver.find_element_by_id("acq").get_attribute("style")
        print("STEP 2 -- 배너 프로세스 그룹 목록 확인")
        if driver.find_element_by_id("acq").get_attribute("style")!="display: none;":
            print("STEP 2 -- ACQ 확인 SUCCESS")
        else:
            print("STEP 2 -- ACQ 확인 FAILED")
            test_details += u"ACQ 프로세스 항목이 존재해야하지만, 표시되지 않음\n"

        if driver.find_element_by_id("man").get_attribute("style")=="display: none;":
            print("STEP 2 -- MAN 확인 SUCCESS")
        else:
            print("STEP 2 -- MAN 확인 FAILED")
            test_details += u"MAN 프로세스 항목이 존재하지 않아야하지만, 표시되어있음\n"
            
        if driver.find_element_by_id("sys").get_attribute("style")!="display: none;":
            print("STEP 2 -- SYS 확인 SUCCESS")
        else:
            print("STEP 2 -- SYS 확인 FAILED")
            test_details += u"SYS 프로세스 항목이 존재해야하지만, 표시되지 않음\n"
            
        if driver.find_element_by_id("swe").get_attribute("style")!="display: none;":
            print("STEP 2 -- SWE 확인 SUCCESS")
        else:
            print("STEP 2 -- SWE 확인 FAILED")
            test_details += u"SWE 프로세스 항목이 존재해야하지만, 표시되지 않음\n"
        
        if driver.find_element_by_id("sup").get_attribute("style")!="display: none;":
            print("STEP 2 -- SUP 확인 SUCCESS")
        else:
            print("STEP 2 -- SUP 확인 FAILED")
            test_details += u"SUP 프로세스 항목이 존재해야하지만, 표시되지 않음\n"
            
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
            
        pi.delete_project(self, "TC_0031")
        
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
