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
tc_content = u"작업 추가에서 프로젝트 기간에 벗어나는 일정을 등록했을 경우, 하단에 '프로젝트 내의 기간을 선택해 주세요.' 라는 문구가 출력되어야 한다. "

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
        
        project_name = "TC_0025"
        
        project_start_date = "2022-08-02"
        project_end_date = "2023-08-02"
        
        work_start_date = "2022-08-02"
        work_end_date = "2024-08-23"
        
        user_id = "admin"
        user_pw = "suresoft"
        
        print("STEP 1 -- 프로젝트 세팅")
        print("STEP 1-1 -- 사용자 로그인 및 프로젝트 등록")
        li.login(self, user_id, user_pw)
        
        # 프로젝트 생성
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "V-SPICE_CAR", project_start_date, project_end_date)
        test_details += pi.create_project(self)
        
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속 후 WBS 페이지로 이동")
        pi.search_project(self, project_name)
        driver.find_element_by_xpath("//a[@id='wbs-tab']/font").click() # WBS 페이지로 이동
        time.sleep(3)
        
        print("STEP 2 -- 작업 추가 일정 오류 확인")
        driver.find_element_by_xpath("//div[@id='ChartVue']/div/div[2]/button/div").click() # 작업 추가 버튼 클릭
        time.sleep(2)
        
        driver.find_element_by_id("wbs-startDate").click()
        time.sleep(1)
        driver.find_element_by_id("wbs-startDate").clear()
        time.sleep(1)
        driver.find_element_by_id("wbs-startDate").send_keys(work_start_date)# 일정 시작일 입력
        time.sleep(2)
        
        driver.find_element_by_id("wbs-endDate").send_keys(work_end_date)
        driver.find_element_by_id("wbs-endDate").send_keys(Keys.ENTER)
        time.sleep(3)
        
        element_text = driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[6]/div[2]/div[2]/span").text
        if element_text == "프로젝트 내의 기간을 선택해 주세요.":
            print("STEP 2 -- SUCCESS")
        else:
            print("STEP 2 -- FAILED")
            test_details+=u"작업 공수가 유효하지 않지만 오류 문구 뜨지 않음\n"
        
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
        pi.delete_project(self, "TC_0025")
        
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
