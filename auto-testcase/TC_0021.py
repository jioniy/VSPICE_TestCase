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
from login import login, logout
from datetime import datetime, timedelta
import unittest, time, re
import os
import inspect
import project_info as pi


tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"프로젝트 이름/기간/기타 정보(차량 명, 아이템, 칩셋, 툴체인)가 프로젝트 등록 시 설정한 프로젝트 정보와 일치해야한다. "

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
        
        project_name = "TC_0021"
        project_start_date = "2022-07-30"
        project_end_date = "2023-07-30"
        project_car = "VPES_CAR"
        project_item = "AA"
        project_chipset = "BB"
        project_toolchain = "CC"

        user_id = "admin"
        user_pw = "suresoft"
        
        print("STEP 1 -- 프로젝트 세팅")
        print("STEP 1-1 -- 사용자 로그인 및 프로젝트 등록")
        login(self, user_id, user_pw)
        
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, project_car, project_start_date, project_end_date)
        test_details += pi.project_extra_info(self, project_item, project_chipset, project_toolchain)
        test_details += pi.create_project(self)
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속")
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
        
        print("STEP 2 -- 프로젝트 키 확인")
        time.sleep(1)
        if driver.find_element_by_id("projectKey").text == project_name:
            print("STEP 2 -- SUCCESS")
        else:
            print("STEP 2 -- FAILED")
            test_details += u"설정한 프로젝트 키와 일치하지 않음\n"
        time.sleep(1)
        
        print("STEP 3 -- 프로젝트 기간 확인")
        time.sleep(1)
        date_to_string = project_start_date +"~"+project_end_date
        if driver.find_element_by_xpath("//div[@id='projectOverView-HeaderVue']/div/div[3]/div[2]").text == date_to_string:
            print("STEP 3 -- SUCCESS")
        else:
            print("STEP 3 -- FAILED")
            test_details += u"설정한 프로젝트 기간과 일치하지 않음\n"
        time.sleep(1)
        
        print("STEP 4 -- 프로젝트 차량 명 확인")
        time.sleep(1)
        if driver.find_element_by_id("projectName").text == project_car:
            print("STEP 4 -- SUCCESS")
        else:
            print("STEP 4 -- FAILED")
            test_details += u"설정한 차량 명과 일치하지 않음\n"
        time.sleep(1)
        
        print("STEP 5 -- 프로젝트 기타 정보 확인")
        print("STEP 5-1 -- 프로젝트 아이템 확인")
        time.sleep(1)
        if driver.find_element_by_id("subName").text == project_item : 
            print("STEP 5-1 -- SUCCESS")
        else:
            print("STEP 5-1 -- FAILED")
            test_details += u"설정한 아이템과 일치하지 않음\n"
        time.sleep(1)
        
        print("STEP 5-2 -- 프로젝트 칩셋 확인")
        time.sleep(1)
        if driver.find_element_by_id("chipset").text == project_chipset : 
            print("STEP 5-2 -- SUCCESS")
        else:
            print("STEP 5-2 -- FAILED")
            test_details += u"설정한 칩셋과 일치하지 않음\n"
        time.sleep(1)
        
        print("STEP 5-3 -- 프로젝트 툴체인 확인")
        time.sleep(1)
        if driver.find_element_by_id("toolchain").text == project_toolchain : 
            print("STEP 5-3 -- SUCCESS")
        else:
            print("STEP 5-3 -- FAILED")
            test_details += u"설정한 툴체인과 일치하지 않음\n"
        time.sleep(1)
        
        
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
        pi.delete_project(self, "TC_0021")
        
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
