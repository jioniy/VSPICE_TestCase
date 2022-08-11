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
from selenium.webdriver.common.action_chains import ActionChains
from login import login, logout
from datetime import datetime, timedelta
import unittest, time, re
import os
import inspect
import project_info as pi


tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"작업의 프로세스 그룹을 변경했을 경우, 해당 작업의 열이 변경한 프로세스 그룹으로 이동해야 한다."

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
        
        project_name = "TC_0030"
        
        user_id = "admin"
        user_pw = "suresoft"
        
        print("STEP 1 -- 프로젝트 세팅")
        print("STEP 1-1 -- 사용자 로그인 및 프로젝트 등록")
        login(self, user_id, user_pw)
        
        # 프로젝트 생성
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "VPES_CAR")
        test_details += pi.create_project(self)
        
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속 후 WBS 페이지로 이동")
        pi.search_project(self, project_name)
        driver.find_element_by_xpath("//a[@id='wbs-tab']/font").click() # WBS 페이지로 이동
        time.sleep(3)
        
        print("STEP 2 -- 작업 프로세스 그룹 변경")
        # 프로세스 그룹 변경 
        
        # 수정 버튼 mouseover 후 클릭 
        actions = ActionChains(driver)
        element_mouseover = driver.find_element_by_xpath("//*[@id='ChartVue']/div[2]/div/div/div[1]/div[1]/div/div[1]/div/div/div[2]/div[4]/div[2]/div")
        element_click = driver.find_element_by_xpath("//*[@id='ChartVue']/div[2]/div/div/div[1]/div[1]/div/div[1]/div/div/div[2]/div[4]/div[2]/div/div[2]/div/label[2]/img")
        
        actions.move_to_element(element_mouseover)# 마우스오버
        actions.click(element_click)# 수정 버튼 클릭
        actions.perform()# 실행
        time.sleep(2)
        
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[2]/div[2]/div/div[2]/span").click()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[2]/div[2]/div/div[3]/ul/li/span").click() # 프로세스 그룹 변경
        time.sleep(2)
        # 일정 입력
        work_start_date = datetime.now().strftime('%Y-%m-%d')
        driver.find_element_by_id("wbs-startDate").click()
        driver.find_element_by_id("wbs-startDate").clear()
        driver.find_element_by_id("wbs-startDate").send_keys(work_start_date)
        time.sleep(2)
        work_end_date_res = datetime.now()+timedelta(days=7)
        work_end_date = work_end_date_res.strftime('%Y-%m-%d')
        driver.find_element_by_id("wbs-endDate").send_keys(work_end_date)
        driver.find_element_by_id("wbs-endDate").send_keys(Keys.ENTER)
        time.sleep(2)
        
        # 공수 입력
        driver.find_element_by_xpath("//input[@type='number']").click()
        driver.find_element_by_xpath("//input[@type='number']").clear()
        driver.find_element_by_xpath("//input[@type='number']").send_keys("2")
        time.sleep(2)
        
        # 변경사항 저장 버튼 클릭
        driver.find_element_by_xpath("//*[@id='wbsRegisterModal']/div/div/div[3]/div/div/button[3]").click()
        
        # '저장에 성공했습니다.' 문구 확인 
        wait = WebDriverWait(driver, 10)
        element_text=""
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
            element_text = driver.find_element_by_id("modal-content").text
        except Exception as e:
            print(e)
        time.sleep(2)
        
        if element_text != u"저장에 성공했습니다.":
            test_details += u"변경 저장 실패\n"
            print("STEP 2 -- FAILED")
        else:
            print("STEP 2 -- SUCCESS")
        time.sleep(2)
        print("STEP 3 -- 작업 위치 확인")
        # 차트 위치 확인 
        element_text_chart = driver.find_element_by_xpath("//div[@id='ChartVue']/div[2]/div/div/div/div/div/div/div/div/div[2]/div[2]/div[2]/div/div[2]/div/label/font").text
        time.sleep(2)
        if element_text_chart=="프로젝트 관리":
            print("STEP 3 -- SUCCESS")
        else:
            print("STEP 3 -- FAILED")
            test_details += u"프로세스 그룹을 ACQ로 변경하였으나 변경되지 않음\n"
    
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
        
        pi.delete_project(self, "TC_0030")
        
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
