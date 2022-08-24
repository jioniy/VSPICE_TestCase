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
from datetime import datetime, timedelta
import unittest, time, re
import os
import inspect
import login_info as li
import project_info as pi


tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"프로젝트 개요 페이지의 프로세스 카드 목록이 프로젝트 등록 시 설정한 프로세스 목록과 동일해야한다."

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
        
        project_name = "TC_0022"
        process_list = ["ACQ.4", "MAN.3", "SWE.1", "SWE.2", "SWE.3", "SWE.4", "SWE.5", "SWE.6", "SUP.1", "SUP.9", "SUP.10"] # whole process - ["ACQ4","MAN3","SYS","SWE","SUP1","SUP8","SUP9", "SUP10"]
        
        user_id = "admin"
        user_pw = "suresoft"
        
        print("STEP 1 -- 프로젝트 세팅")
        print("STEP 1-1 -- 사용자 로그인 및 프로젝트 등록")
        li.login(self, user_id, user_pw)
        
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "V-SPICE_CAR")
        test_details += pi.project_process_info(self, True, True, False, True, True, False, True, True) # SYS, SUP8 프로세스 비활성화
        test_details += pi.create_project(self)
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속")
        pi.search_project(self, project_name)
        
        print("STEP 2 -- 프로세스 목록 확인")
        element_list= driver.find_elements_by_xpath("//*[@id='projectOverView-ProjectStateVue']/div[2]/div[3]/div/div") # return element_list[0], element_list[1],...
        error_list=[] 
        for i in range(len(element_list)):
            if element_list[i].find_element_by_xpath(".//div[1]/div[2]").text != process_list[i]:
                error_list.append(element_list[i].find_element_by_xpath(".//div[1]/div[2]").text)
        time.sleep(2)
        if len(error_list) == 0 :
            print("STEP 2 -- SUCCESS")
        else:
            print("STEP 2 -- FAILED")
            print("오류 항목 : ", end="")
            print(error_list)
        time.sleep(2)
        
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

        # 테스트용 프로젝트 삭제 
        pi.delete_project(self, "TC_0022")
        
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
