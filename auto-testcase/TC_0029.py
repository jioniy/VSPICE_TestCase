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
from login import login, logout, join, delete_user
from datetime import datetime, timedelta
import unittest, time, re
import os
import inspect
import project_info as pi


tc_file = inspect.getfile(inspect.currentframe())
tc_num = os.path.splitext(tc_file)[0]
tc_content = u"작업의 필수 정보를 변경했을 경우, 변경한 필수 정보가 WBS 페이지에 반영되어야 한다. "

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
        
        project_name = "TC_0029"
        
        user_id = "admin"
        user_pw = "suresoft"
        
        wm_user_id = "test_wm"
        wm_user_name = u"홍길동"
        wm_user_email = "testwm@naver.com"
        wm_user_pw = "1q2w3e!!"
        wm_user_pw_ck = "1q2w3e!!"
        
        print("STEP 1 -- 프로젝트 세팅")
        print("STEP 1-1 -- 담당자 테스트용 사용자 생성")
        join(self, wm_user_id, wm_user_name, wm_user_email, wm_user_pw, wm_user_pw_ck)
        
        print("STEP 1-2 -- 사용자 로그인 및 프로젝트 등록")
        login(self, user_id, user_pw)
        
        # 프로젝트 생성
        test_details += pi.project_essential_info(self, "GIT", "http://vpes@192.168.0.136:7990/scm/sprin/vpes.git", "vpes", "suresoft", project_name, "VPES_CAR")
        test_details += pi.project_user_info(self, ["test_wm"])
        test_details += pi.create_project(self)
        
        time.sleep(2)
        
        print("STEP 1-2 -- 프로젝트 접속 후 WBS 페이지로 이동")
        pi.search_project(self, project_name)
        driver.find_element_by_xpath("//a[@id='wbs-tab']/font").click() # WBS 페이지로 이동
        time.sleep(3)
        
        print("STEP 2 -- WBS 작업 추가")
        driver.find_element_by_xpath("//div[@id='ChartVue']/div/div[2]/button/div/div/img").click() # 작업 추가 버튼 클릭
        time.sleep(1) 
        driver.find_element_by_xpath("//input[@type='text']").click()
        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("ACQ_WORK_0029") # 작업명 등록
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

        
        print("STEP 3 -- WBS 작업 변경")
        # 수정 버튼 mouseover 후 클릭 
        actions = ActionChains(driver)
        element_mouseover = driver.find_element_by_xpath("//*[@id='ChartVue']/div[2]/div/div/div[1]/div[1]/div/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div")
        element_click = driver.find_element_by_xpath("//*[@id='ChartVue']/div[2]/div/div/div[1]/div[1]/div/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div/label[2]/img")
        
        actions.move_to_element(element_mouseover)# 마우스오버
        actions.click(element_click)# 수정 버튼 클릭
        actions.perform()# 실행
        time.sleep(2)
        
        driver.find_element_by_xpath("//input[@type='text']").click()
        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("MAN_WORK_0029")# 작업명 변경
        time.sleep(1) 
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[2]/div[2]/div/div[2]/span").click()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[2]/div[2]/div/div[3]/ul/li[2]/span").click() # 프로세스 그룹 변경
        time.sleep(1) 
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[4]/div[2]/div/div[2]/span/div").click()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[4]/div[2]/div/div[3]/ul/li[2]/span/div/span").click()# 담당자(work manager) 변경
        time.sleep(1) 
        # 일정 시작일 입력
        work_start_date_res = datetime.now()+timedelta(days=10)
        work_start_date = work_start_date_res.strftime('%Y-%m-%d')
        driver.find_element_by_id("wbs-startDate").click()
        driver.find_element_by_id("wbs-startDate").clear()
        time.sleep(1)
        driver.find_element_by_id("wbs-startDate").send_keys(work_start_date)
        time.sleep(2)
        # 일정 종료일 입력
        work_end_date_res = datetime.now()+timedelta(days=20)
        work_end_date = work_end_date_res.strftime('%Y-%m-%d')
        driver.find_element_by_id("wbs-endDate").send_keys(work_end_date)
        driver.find_element_by_id("wbs-endDate").send_keys(Keys.ENTER)
        time.sleep(2)
        
        driver.find_element_by_xpath("//input[@type='number']").clear()
        driver.find_element_by_xpath("//input[@type='number']").send_keys("2") # 공수 변경
        
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[8]/div[2]/div/textarea").click()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[8]/div[2]/div/textarea").click()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[8]/div[2]/div/textarea").clear()
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[2]/div/div[8]/div[2]/div/textarea").send_keys(u"작업 내용 수정") # 사유 입력
        
        driver.find_element_by_xpath("//div[@id='wbsRegisterModal']/div/div/div[3]/div/div/button[3]").click()
        
        wait = WebDriverWait(driver, 10)
        element_text=""
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'alertModal')))
            element_text = driver.find_element_by_id("modal-content").text
        except Exception as e:
            print(e)
        time.sleep(2)
        
        if element_text != u"저장에 성공했습니다.":
            test_details += u"작업 변경 실패\n"
            print("STEP 3 -- 작업 변경 FAILED")
        else:
            print("STEP 3 -- 작업 변경 SUCCESS")
        time.sleep(2)
        
        print("STEP 3 -- WBS 작업 변경 확인")
        element_work_name = driver.find_element_by_xpath("//div[@id='ChartVue']/div[2]/div/div/div/div/div/div/div/div/div[2]/div[5]/div[2]/div/div[2]/div/label/font").text# wbs 작업명 확인 (+ 위치 확인에 따른 상위 프로세스 확인)
        element_work_status = driver.find_element_by_xpath("//div[@id='ChartVue']/div[2]/div/div/div/div/div/div/div/div/div[2]/div[5]/div[3]/div/div/div").text # wbs 작업 상태 확인
        element_work_wm = driver.find_element_by_xpath("//div[@id='ChartVue']/div[2]/div/div/div/div/div/div/div/div/div[2]/div[5]/div[4]/div/div/div/font").text # wbs 담당자 확인
        element_work_num = driver.find_element_by_xpath("//div[@id='ChartVue']/div[2]/div/div/div/div/div/div/div/div/div[2]/div[5]/div[5]/div/div/div").text # wbs 공수 확인
        
        if element_work_name == "MAN_WORK_0029":
            print("STEP 3 -- 작업명 수정 SUCCESS")
        else:
            print("STEP 3 -- 작업명 수정 FAILED")
            test_details += u"작업명을 수정하였으나, wbs 페이지에서 수정된 작업명이 반영되지 않음\n"
        time.sleep(1)
        if element_work_status == u"예정":
            print("STEP 3 -- 작업 상태 수정 SUCCESS")
        else:
            print("STEP 3 -- 작업 상태 수정 FAILED")
            test_details += u"작업 상태를 수정하였으나, wbs 페이지에서 수정된 작업 상태가 반영되지 않음\n"
        time.sleep(1)   
        if element_work_wm == u"홍길동":
            print("STEP 3 -- 작업 담당자 수정 SUCCESS")
        else:
            print("STEP 3 -- 작업 담당자 수정 FAILED")  
            test_details += u"작업 담당자를 수정하였으나, wbs 페이지에서 수정된 작업 담당자가 반영되지 않음\n"
        time.sleep(1) 
        if element_work_num == "2":
            print("STEP 3 -- 작업 공수 수정 SUCCESS")
        else:
            print("STEP 3 -- 작업 공수 수정 FAILED")  
            test_details += u"작업 공수를 수정하였으나, wbs 페이지에서 수정된 작업 공수가 반영되지 않음\n"
        time.sleep(1) 

        if self.is_element_present(By.XPATH, "//*[@id='ChartVue']/div[2]/div/div/div[1]/div[1]/div/div[1]/div/div/div[2]/div[5]/div[6]/div/div/div/a/img")==True: # 작업 변경 내역 아이콘 확인
            print("STEP 3 -- 작업 변경 내역 아이콘 확인 SUCCESS")
            driver.find_element_by_xpath("//*[@id='ChartVue']/div[2]/div/div/div[1]/div[1]/div/div[1]/div/div/div[2]/div[5]/div[6]/div/div/div/a/img").click()
            
            popover_id = driver.find_element_by_xpath("//*[@id='ChartVue']/div[2]/div/div/div[1]/div[1]/div/div[1]/div/div/div[2]/div[5]/div[6]/div/div/div/a").get_attribute("aria-describedby") #팝오버 창의 id 가져오기
            print(popover_id)
            print("STEP 3 -- 작업 변경 내역 열람 SUCCESS")
            if driver.find_element_by_xpath("//div[@id='" + popover_id + "']/div[2]/div/table/tbody/tr[2]/td[2]").text == u"홍길동\ntest_wm": # 변경 내용 담당자 확인
                print("STEP 3 -- 작업 변경 내역 담당자 열람 SUCCESS")
            else:
                print("STEP 3 -- 작업 변경 내역 담당자 열람 FAILED")
                test_details += u"작업 담당자를 수정하였으나, 작업 변경 내역에서 수정된 작업 담당자가 반영되지 않음\n"
            time.sleep(1) 
            if driver.find_element_by_xpath("//div[@id='" + popover_id + "']/div[2]/div/table/tbody/tr[2]/td[3]").text == "2 MD": # 변경 내용 공수 확인
                print("STEP 3 -- 작업 변경 내역 공수 열람 SUCCESS")
            else:
                print("STEP 3 -- 작업 변경 내역 공수 열람 FAILED")
                test_details += u"작업 공수를 수정하였으나, 작업 변경 내역에서 수정된 작업 공수가 반영되지 않음\n"
            time.sleep(1) 
            date_text = work_start_date + " - " + work_end_date
            print(driver.find_element_by_xpath("//div[@id='" + popover_id + "']/div[2]/div/table/tbody/tr[2]/td[4]").text)
            if driver.find_element_by_xpath("//div[@id='" + popover_id + "']/div[2]/div/table/tbody/tr[2]/td[4]").text == date_text: # 변경 내용 일정 확인
                print("STEP 3 -- 작업 변경 내역 일정 열람 SUCCESS")
            else:
                print("STEP 3 -- 작업 변경 내역 일정 열람 FAILED")
                test_details += u"작업 일정을 수정하였으나, 작업 변경 내역에서 수정된 작업 일정이 반영되지 않음\n"
            time.sleep(1) 
            if driver.find_element_by_xpath("//div[@id='" + popover_id + "']/div[2]/div/table/tbody/tr[2]/td[5]").text == u"작업 내용 수정": # 변경 사유 확인
                print("STEP 3 -- 작업 변경 내역 사유 열람 SUCCESS")
            else:
                print("STEP 3 -- 작업 변경 내역 사유 열람 FAILED")
                test_details += u"변경 사유를 입력하였으나, 작업 변경 내역에서 반영되지 않음\n"
            time.sleep(1) 
            
        else: #작업 변경 내역 아이콘 없음
            print("STEP 3 -- 작업 변경 내역 아이콘 확인 FAILED")
            test_details += u"작업을 변경하였으나, 작업 변경 내역 아이콘을 볼 수 없음\n"
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
        
        pi.delete_project(self, "TC_0029")
        delete_user(self, "test_wm")
        
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
