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
import project_info as pi
from datetime import datetime, timedelta
import unittest, time, re
import os
import inspect


tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"프로젝트의 기간에 오늘 일자가 포함될 때, '진행중' 이라는 아이콘이 떠야 한다."

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
        
        print("STEP 1 -- 테스트용 프로젝트 등록")
        project_name = "TC_0016"
        
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date_res = datetime.now()+timedelta(days=7)
        end_date = end_date_res.strftime('%Y-%m-%d')
        
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "VPES_CAR", start_date, end_date)
        test_details += pi.create_project(self)
        
        print("STEP 1 -- 프로젝트 검색 및 클릭")
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
        
        print("STEP 2 -- 배너 프로젝트 진행 상태 확인")
        # 프로젝트 배너 - 프로젝트 진행상태 가져오기
        element_text=driver.find_element_by_xpath("//*[@id='projectSideBar']/div/span[1]").text
        if element_text!="진행중":
            print("STEP 2 -- FAILED")
            test_details+=u"프로젝트가 진행 중이지만 올바른 진행상태 표시 안됨\n"
        else:
            print("STEP 2 -- SUCCESS")
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
            
        pi.delete_project(self, "TC_0016")
        
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
