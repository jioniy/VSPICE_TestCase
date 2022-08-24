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
tc_content = u"WBS 작업 일정을 추가 또는 변경했을 경우 MAN 프로세스의 일정, 업무 분해 구조도가 활성화되어야 한다. "

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
        
        project_name = "TC_0034"
        
        user_id = "admin"
        user_pw = "suresoft"
        
        print("STEP 1 -- 프로젝트 세팅")
        
        print("STEP 1-1 -- 사용자 로그인 및 프로젝트 등록")
        li.login(self, user_id, user_pw)
        
        # 프로젝트 생성
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "V-SPICE_CAR")
        test_details += pi.create_project(self)
        
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속 후 WBS 페이지로 이동")
        pi.search_project(self, project_name)
        driver.find_element_by_id('wbs-tab').click() # WBS 페이지로 이동
        time.sleep(3)
        
        print("STEP 2 -- WBS 작업 추가")
        driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);") 
        time.sleep(1)
        driver.find_element_by_xpath("//div[@id='ChartVue']/div/div[2]/button/div/div/img").click() # 작업 추가 버튼 클릭
        time.sleep(1) 
        driver.find_element_by_xpath("//input[@type='text']").click()
        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("ACQ_WORK_0034") # 작업명 등록
        time.sleep(1)
        
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[2]/div[2]/div/div[2]/span").click()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[2]/div[2]/div/div[3]/ul/li/span").click()# 프로세스 그룹 등록
        time.sleep(1) 
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[4]/div[2]/div/div[2]").click()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[4]/div[2]/div/div[3]/ul/li/span/div").click() # 담당자(work manager) 등록
        time.sleep(1) 
        # 일정 시작일 입력
        work_start_date_res = datetime.now()+timedelta(days=-10)
        work_start_date = work_start_date_res.strftime('%Y-%m-%d')
        driver.find_element_by_id("wbs-startDate").click()
        driver.find_element_by_id("wbs-startDate").clear()
        time.sleep(1)
        driver.find_element_by_id("wbs-startDate").send_keys(work_start_date)
        time.sleep(2)
        # 일정 종료일 입력
        work_end_date_res = datetime.now()+timedelta(days=10)
        work_end_date = work_end_date_res.strftime('%Y-%m-%d')
        driver.find_element_by_id("wbs-endDate").send_keys(work_end_date)
        driver.find_element_by_id("wbs-endDate").send_keys(Keys.ENTER)
        time.sleep(2)
        
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[3]/div/div/button[2]").click() # 작업 등록 완료 
        
        wait = WebDriverWait(driver, 10)
        element_text=""
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
            element_text = driver.find_element_by_id("modal-content").text
        except Exception as e:
            print(e)
        time.sleep(2)
        
        if element_text != u"저장에 성공했습니다.":
            test_details += u"작업 저장 실패\n"
            print("STEP 2 -- FAILED")
        else:
            print("STEP 2 -- SUCCESS")
        time.sleep(2)
        
        print("STEP 3 -- MAN 프로세스 확인")
        print("STEP 3-1 -- MAN 페이지로 이동")
        driver.find_element_by_id("processes-tab").click()
        driver.find_element_by_id("man").click()
        time.sleep(3)
        
        print("STEP 3-2 -- MAN 프로세스 일정/업무 분해 구조도 활성화 확인")
        # 체크 아이콘
        check_status_1 = driver.find_element_by_xpath("//*[@id='processDetail-ReportVue']/div[2]/ul/li[6]/div[1]").get_attribute("class") # 일정
        check_status_2 = driver.find_element_by_xpath("//*[@id='processDetail-ReportVue']/div[2]/ul/li[7]/div[1]").get_attribute("class") # 업무분해 구조도

        # 작업 산출물 분류 이름
        text_status_1 = driver.find_element_by_xpath("//*[@id='processDetail-ReportVue']/div[2]/ul/li[6]/div[3]").get_attribute("class") # 일정
        text_status_2 = driver.find_element_by_xpath("//*[@id='processDetail-ReportVue']/div[2]/ul/li[7]/div[3]").get_attribute("class") # 업무분해 구조도

        if check_status_1 == "process-detail-check-icon" and text_status_1.find("workproduct-not-upload")==-1:
            print("STEP 3-2 -- 프로세스 일정 활성화 SUCCESS")
        else:
            print("STEP 3-2 -- 프로세스 일정 활성화 FAILED")
            test_details += u"WBS 작업이 추가되었지만 MAN 프로세스의 일정이 활성화되지 않음.\n"
        time.sleep(1)
        
        if check_status_2 == "process-detail-check-icon" and text_status_2.find("workproduct-not-upload")==-1:
            print("STEP 3-2 -- 프로세스 업무 분해 구조도 활성화 SUCCESS")
        else:
            print("STEP 3-2 -- 프로세스 업무 분해 구조도 활성화 FAILED")
            test_details += u"WBS 작업이 추가되었지만 MAN 프로세스의 업무 분해 구조도가 활성화되지 않음.\n"
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
            
        pi.delete_project(self, "TC_0034")
        
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
